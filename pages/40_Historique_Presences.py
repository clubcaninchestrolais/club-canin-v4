import streamlit as st
from supabase_rest import supabase

st.set_page_config(page_title="Historique des présences", page_icon="📘")
st.title("📘 Historique des présences d’un membre")

# ---------------------------------------------------------
# 1. Sélection du membre
# ---------------------------------------------------------
membres = (
    supabase.table("membres")
    .select("*")
    .order("nom")
    .execute()
    .data
)

choix_membre = st.selectbox(
    "Choisir un membre",
    options=membres,
    format_func=lambda m: f"{m['nom']} {m['prenom']}"
)

membre_id = choix_membre["id"]

st.markdown("---")

# ---------------------------------------------------------
# 2. Charger les présences du membre
# ---------------------------------------------------------
presences = (
    supabase.table("cours_presences")
    .select("*")
    .eq("membre_id", membre_id)
    .order("date_presence", desc=True)
    .execute()
    .data
)

if not presences:
    st.info("Aucune présence enregistrée pour ce membre.")
    st.stop()

# ---------------------------------------------------------
# 3. Construire l’historique détaillé
# ---------------------------------------------------------
historique = []

for p in presences:

    # Charger séance
    seance = (
        supabase.table("cours_seances")
        .select("*")
        .eq("id", p["seance_id"])
        .execute()
        .data[0]
    )

    # Charger cours
    cours = (
        supabase.table("cours")
        .select("*")
        .eq("id", p["cours_id"])
        .execute()
        .data[0]
    )

    # Charger chien
    chien = (
        supabase.table("chiens")
        .select("*")
        .eq("id", p["chien_id"])
        .execute()
        .data[0]
    )

    historique.append({
        "Date": p["date_presence"],
        "Cours": cours["nom"],
        "Heure": seance["heure_debut"],
        "Chien": chien["nom"],
        "Statut": p["statut"]
    })

# ---------------------------------------------------------
# 4. Affichage
# ---------------------------------------------------------
st.subheader("Historique complet")

st.dataframe(historique, use_container_width=True)
