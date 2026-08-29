import streamlit as st
from supabase import create_client
import datetime

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("Validation des présences")

# ---------------------------------------------------------
# Charger les cours
# ---------------------------------------------------------
cours = (
    supabase.table("cours")
    .select("*")
    .order("nom")
    .execute()
    .data
)

cours_labels = {c["nom"]: c["id"] for c in cours}
cours_nom = st.selectbox("Filtrer par cours :", list(cours_labels.keys()))
cours_id = cours_labels[cours_nom]

# ---------------------------------------------------------
# Charger les séances du cours sélectionné
# ---------------------------------------------------------
seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("cours_id", cours_id)
    .order("date_seance")
    .execute()
    .data
)

if not seances:
    st.info("Aucune séance pour ce cours.")
    st.stop()

seance_labels = {
    f"{s['nom_seance']} — {s['date_seance']}": s["id"]
    for s in seances
}

seance_nom = st.selectbox("Séance :", list(seance_labels.keys()))
seance_id = seance_labels[seance_nom]

# ---------------------------------------------------------
# Charger les inscriptions à cette séance
# ---------------------------------------------------------
inscriptions = (
    supabase.table("cours_inscriptions")
    .select("*, membres(*), chiens(*)")
    .eq("seance_id", seance_id)
    .execute()
    .data
)

if not inscriptions:
    st.info("Aucun inscrit pour cette séance.")
    st.stop()

st.subheader("Liste des inscrits")

# ---------------------------------------------------------
# Affichage + validation
# ---------------------------------------------------------
for ins in inscriptions:

    membre = ins["membres"]
    chien = ins["chiens"]

    membre_nom = f"{membre['prenom']} {membre['nom']}"
    chien_nom = chien["nom"] if chien else "(bénévole)"

    st.write(f"**{membre_nom}** — 🐶 {chien_nom}")

    # Vérifier si présence déjà validée
    presence = (
        supabase.table("cours_presences")
        .select("*")
        .eq("membre_id", membre["id"])
        .eq("seance_id", seance_id)
        .execute()
        .data
    )

    if presence:
        st.success("Présence déjà validée")
        continue

    # Bouton de validation
    if st.button(f"Valider présence — {membre_nom}"):

        # ---------------------------------------------------------
        # 1) Enregistrer la présence
        # ---------------------------------------------------------
        supabase.table("cours_presences").insert({
            "membre_id": membre["id"],
            "chien_id": chien["id"] if chien else None,
            "seance_id": seance_id,
            "present": True,
            "date_presence": datetime.date.today().isoformat()
        }).execute()

        # ---------------------------------------------------------
        # 2) Décrémenter l'abonnement du membre
        # ---------------------------------------------------------
        abo = (
            supabase.table("abonnements")
            .select("*")
            .eq("membre_id", membre["id"])
            .eq("actif", True)
            .execute()
            .data
        )

        if abo:
            abo = abo[0]
            reste = abo["seances_restantes"] - 1

            supabase.table("abonnements").update({
                "seances_restantes": reste,
                "date_dernier_cours": datetime.date.today().isoformat(),
                "cours_id_dernier": cours_id,
                "actif": reste > 0
            }).eq("id", abo["id"]).execute()

        st.success("Présence validée")
        st.experimental_rerun()
