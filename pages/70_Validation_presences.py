import streamlit as st
from supabase import create_client, Client
import datetime

# Connexion Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Validation des présences")

# Séance du jour
aujourdhui = datetime.date.today().isoformat()

seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("date_seance", aujourdhui)
    .execute()
    .data
)

if not seances:
    st.info("Aucune séance aujourd'hui.")
    st.stop()

seance = seances[0]
seance_id = seance["id"]

st.subheader(f"Séance du jour : {seance['nom_seance']}")

# ---------------------------------------------------------
# 1️⃣ EXTÉRIEURS VALIDÉS
# ---------------------------------------------------------
exterieurs = (
    supabase.table("preinscriptions")
    .select("*")
    .eq("seance_id", seance_id)
    .eq("acceptee", True)
    .execute()
    .data
)

# ---------------------------------------------------------
# 2️⃣ MEMBRES INSCRITS
# ---------------------------------------------------------
inscriptions = (
    supabase.table("cours_seances_inscriptions")
    .select("*")
    .eq("seance_id", seance_id)
    .eq("actif", True)
    .execute()
    .data
)

membres_inscrits = []
for ins in inscriptions:
    membre = (
        supabase.table("membres")
        .select("*")
        .eq("id", ins["membre_id"])
        .execute()
        .data
    )
    chien = (
        supabase.table("chiens")
        .select("*")
        .eq("id", ins["chien_id"])
        .execute()
        .data
    )

    if membre and chien:
        membres_inscrits.append({
            "inscription_id": ins["id"],
            "membre": membre[0],
            "chien": chien[0],
            "cours": seance["nom_seance"]
        })

# ---------------------------------------------------------
# 🔍 FILTRE TEXTE
# ---------------------------------------------------------
filtre = st.text_input("🔍 Rechercher un membre (nom, prénom, chien)")

if filtre:
    f = filtre.lower()
    membres_inscrits = [
        m for m in membres_inscrits
        if f in m["membre"]["nom"].lower()
        or f in m["membre"]["prenom"].lower()
        or f in m["chien"]["nom"].lower()
    ]

# ---------------------------------------------------------
# 🅰️ TRI ALPHABÉTIQUE
# ---------------------------------------------------------
membres_inscrits = sorted(
    membres_inscrits,
    key=lambda x: (x["membre"]["nom"].lower(), x["membre"]["prenom"].lower())
)

# ---------------------------------------------------------
# 🐾 REGROUPEMENT PAR COURS
# ---------------------------------------------------------
cours_groupes = {}
for item in membres_inscrits:
    cours = item["cours"]
    if cours not in cours_groupes:
        cours_groupes[cours] = []
    cours_groupes[cours].append(item)

# ---------------------------------------------------------
# AFFICHAGE
# ---------------------------------------------------------
st.markdown("### Participants à valider")

# ---------------------------------------------------------
# EXTÉRIEURS
# ---------------------------------------------------------
for ext in exterieurs:
    st.write(f"🟦 Extérieur : {ext['prenom']} {ext['nom']} – {ext['chien_nom']}")

    if ext.get("present_exterieur"):
        st.success("Présence déjà validée.")
        continue

    if st.button(
        f"Valider présence extérieur {ext['id']}",
        key=f"btn_ext_{ext['id']}"
    ):
        insertion = (
            supabase.table("preinscriptions")
            .update({"present_exterieur": True})
            .eq("id", ext["id"])
            .select("*")
            .execute()
        )

        if insertion.data:
            st.success("Présence extérieur validée.")
            st.rerun()
        else:
            st.error("❌ Erreur lors de la validation.")
            st.write(insertion)

# ---------------------------------------------------------
# 🐾 MEMBRES PAR COURS
# ---------------------------------------------------------
for cours, liste in cours_groupes.items():

    st.markdown(f"## 🐾 {cours}")

    for item in liste:
        membre = item["membre"]
        chien = item["chien"]

        # ---------------------------------------------------------
        # 💳 Vérifier cotisation active
        # ---------------------------------------------------------
        cotisations = (
            supabase.table("cotisations")
            .select("*")
            .eq("membre_id", membre["id"])
            .execute()
            .data
        )

        cot_active = [
            c for c in cotisations
            if c["statut"] == "active" and c["paye"] == True
        ]

        cot_msg = "💳 Cotisation active" if cot_active else "❌ Cotisation non active"

        # ---------------------------------------------------------
        # 🎫 Vérifier abonnement actif
        # ---------------------------------------------------------
        abos = (
            supabase.table("abonnements")
            .select("*")
            .eq("membre_id", membre["id"])
            .order("id", desc=True)
            .execute()
            .data
        )

        if abos:
            abo = abos[0]
            rest = abo["seances_restantes"]

            if rest == 0:
                couleur = "#ffcccc"
                abo_msg = "❌ Abonnement terminé"
            elif rest <= 2:
                couleur = "#ffe6cc"
                abo_msg = f"⚠️ {rest} séance(s) restante(s)"
            else:
                couleur = "#e6ffe6"
                abo_msg = f"🟢 {rest} séances restantes"
        else:
            couleur = "#ffcccc"
            abo_msg = "❌ Aucun abonnement"

        # ---------------------------------------------------------
        # Vérifier si déjà validé
        # ---------------------------------------------------------
        presence = (
            supabase.table("cours_presences")
            .select("*")
            .eq("membre_id", membre["id"])
            .eq("chien_id", chien["id"])
            .eq("seance_id", seance_id)
            .execute()
            .data
        )

        deja = bool(presence)

        # ---------------------------------------------------------
        # AFFICHAGE COMPACT
        # ---------------------------------------------------------
        st.markdown(
            f"""
            <div style='background:{couleur};padding:10px;border-radius:6px;margin-bottom:6px;'>
            <b>{membre['prenom']} {membre['nom']}</b> – {chien['nom']}  
            <br>{cot_msg} | {abo_msg}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------------------------------------------------------
        # BOUTON
        # ---------------------------------------------------------
        if deja:
            st.success("Présence déjà validée.")
            continue

        if "terminé" in abo_msg.lower():
            st.error("Validation impossible : abonnement terminé.")
            continue

        if st.button(
            f"Valider présence {item['inscription_id']}",
            key=f"btn_membre_{item['inscription_id']}"
        ):
            insertion = supabase.table("cours_presences").insert({
                "membre_id": membre["id"],
                "chien_id": chien["id"],
                "seance_id": seance_id,
                "date_presence": aujourdhui,
                "present": True
            }).execute()

            if insertion.data:
                st.success("Présence validée.")
                st.rerun()
            else:
                st.error("❌ Erreur lors de l'enregistrement.")
                st.write(insertion)
