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

# ---------------------------------------------------------
# 🔥 Charger toutes les séances puis filtrer par date
# ---------------------------------------------------------
seances_raw = (
    supabase.table("cours_seances")
    .select("*")
    .order("id")
    .execute()
    .data
)

seances = [
    s for s in seances_raw
    if s["date_seance"][:10] == aujourdhui
]

if not seances:
    st.info("Aucune séance aujourd'hui.")
    st.stop()

# ---------------------------------------------------------
# 🔁 BOUCLE SUR TOUTES LES SÉANCES DU JOUR
# ---------------------------------------------------------
for seance in seances:

    seance_id = int(seance["id"])
    nom_seance = seance["nom_seance"]

    st.markdown(f"### 🐾 {nom_seance} — {seance['date_seance'][:10]}")

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
    # 2️⃣ MEMBRES INSCRITS (cours_inscriptions)
    # ---------------------------------------------------------
    inscriptions_raw = (
        supabase.table("cours_inscriptions")
        .select("*")
        .execute()
        .data
    )

    inscriptions = [
        ins for ins in inscriptions_raw
        if int(ins["seance_id"]) == seance_id
    ]

    membres_inscrits = []
    for ins in inscriptions:

        try:
            membre_id = int(ins["membre_id"])
            chien_id = int(ins["chien_id"])
            seance_id_ins = int(ins["seance_id"])
        except:
            continue

        membre = (
            supabase.table("membres")
            .select("*")
            .eq("id", membre_id)
            .execute()
            .data
        )
        chien = (
            supabase.table("chiens")
            .select("*")
            .eq("id", chien_id)
            .execute()
            .data
        )

        if not membre or not chien:
            continue

        membres_inscrits.append({
            "inscription_id": ins["id"],
            "membre": membre[0],
            "chien": chien[0],
            "seance_id": seance_id_ins
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
    # AFFICHAGE EXTÉRIEURS
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

    # ---------------------------------------------------------
    # AFFICHAGE MEMBRES (STYLE COMME AVANT)
    # ---------------------------------------------------------
    for item in membres_inscrits:
        membre = item["membre"]
        chien = item["chien"]
        seance_id = int(item["seance_id"])

        # Vérifier présence
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

        # Vérifier cotisation
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

        # Vérifier abonnement
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

        # Bloc stylé comme avant
        st.markdown(
            f"""
            <div style='background:{couleur};
                        padding:12px;
                        border-radius:8px;
                        margin-bottom:10px;
                        border:1px solid #ddd;'>

                <b>{membre['prenom']} {membre['nom']}</b><br>
                🐶 {chien['nom']}<br>
                {cot_msg} | {abo_msg}

            </div>
            """,
            unsafe_allow_html=True
        )

        # Bouton
        if deja:
            st.success("Présence déjà validée.")
            continue

        if "terminé" in abo_msg.lower():
            st.error("Validation impossible : abonnement terminé.")
            continue

        if st.button(
            f"Valider présence de {membre['prenom']} {membre['nom']}",
            key=f"btn_membre_{item['inscription_id']}"
        ):
            insertion = supabase.table("cours_presences").insert({
                "membre_id": membre["id"],
                "chien_id": chien["id"],
                "seance_id": seance_id,
                "present": True
            }).execute()

            if insertion.data:
                st.success("Présence validée.")
                st.rerun()

