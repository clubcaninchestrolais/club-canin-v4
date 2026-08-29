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

# Charger TOUTES les séances du jour
seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("date_seance", aujourdhui)
    .order("id")
    .execute()
    .data
)

if not seances:
    st.info("Aucune séance aujourd'hui.")
    st.stop()

st.markdown("## 🐾 Séances du jour")

# ---------------------------------------------------------
# 🔁 BOUCLE SUR TOUTES LES SÉANCES DU JOUR
# ---------------------------------------------------------
for seance in seances:

    seance_id = seance["id"]
    nom_seance = seance["nom_seance"]

    st.markdown(f"### 🐾 {nom_seance} — {seance['date_seance']}")

    # ---------------------------------------------------------
    # 1️⃣ EXTÉRIEURS VALIDÉS (inchangé)
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
    # 2️⃣ MEMBRES INSCRITS (NOUVEAU : cours_inscriptions)
    # ---------------------------------------------------------
    inscriptions = (
        supabase.table("cours_inscriptions")
        .select("*")
        .eq("seance_id", seance_id)
        .execute()
        .data
    )

    membres_inscrits = []
    for ins in inscriptions:

        # 🔒 Protection anti-NULL
        if not ins["membre_id"] or not ins["chien_id"]:
            continue

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

        if not membre or not chien:
            continue

        membres_inscrits.append({
            "inscription_id": ins["id"],
            "membre": membre[0],
            "chien": chien[0],
            "cours": nom_seance
        })

    # ---------------------------------------------------------
    # 🔍 FILTRE TEXTE
    # ---------------------------------------------------------
    filtre = st.text_input(
        f"🔍 Rechercher un membre dans {nom_seance}",
        key=f"filtre_{seance_id}"
    )

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
    # AFFICHAGE EXTÉRIEURS (inchangé)
    # ---------------------------------------------------------
    for ext in exterieurs:

        if not ext["nom"] or not ext["prenom"] or not ext["chien_nom"]:
            continue

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
    # AFFICHAGE MEMBRES (corrigé)
    # ---------------------------------------------------------
    for item in membres_inscrits:
        membre = item["membre"]
        chien = item["chien"]

        # ---------------------------------------------------------
        # 💳 Vérifier cotisation active
        # ---------------------------------------------------------
        cotisations = (
            supabase.table("cotisations")
            .select("*")
            .eq("id_membre", membre["id"])
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
            .eq("id_membre", membre["id"])
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
        # Vérifier si déjà validé (cours_presences)
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

