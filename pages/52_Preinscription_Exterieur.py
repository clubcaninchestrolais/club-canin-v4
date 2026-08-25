import streamlit as st
from supabase_rest import supabase

st.set_page_config(page_title="Préinscription extérieur", page_icon="🐾")
st.title("🐾 Préinscription pour une personne extérieure")

st.markdown("Veuillez remplir ce formulaire pour participer à une séance du club.")

# ---------------------------------------------------------
# 1. Informations personnelles
# ---------------------------------------------------------
st.subheader("Vos informations")

nom = st.text_input("Nom")
prenom = st.text_input("Prénom")
email = st.text_input("Email")
telephone = st.text_input("Téléphone")

# Anti‑robot simple
anti_bot = st.text_input("Écrivez le mot 'chien' pour confirmer que vous êtes humain")

# ---------------------------------------------------------
# 2. Informations du chien
# ---------------------------------------------------------
st.subheader("Votre chien")

chien_nom = st.text_input("Nom du chien")
chien_race = st.text_input("Race du chien")

# ---------------------------------------------------------
# 3. Choix du cours et de la séance
# ---------------------------------------------------------
st.subheader("Cours souhaité")

cours = (
    supabase.table("cours")
    .select("*")
    .order("nom")
    .execute()
    .data
)

choix_cours = st.selectbox(
    "Choisir un cours",
    options=cours,
    format_func=lambda c: c["nom"]
)

seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("cours_id", choix_cours["id"])
    .order("date_seance")
    .execute()
    .data
)

choix_seance = st.selectbox(
    "Choisir une séance",
    options=seances,
    format_func=lambda s: f"{s['date_seance']} — {s['heure_debut']}"
)

# ---------------------------------------------------------
# 4. Validation du formulaire
# ---------------------------------------------------------
if st.button("Envoyer la préinscription"):

    # Champs obligatoires
    if not nom or not prenom or not email or not telephone or not chien_nom or not chien_race:
        st.error("Veuillez remplir tous les champs obligatoires.")
        st.stop()

    # Anti‑robot
    if anti_bot.lower().strip() != "chien":
        st.error("Veuillez écrire le mot 'chien' pour confirmer que vous êtes humain.")
        st.stop()

    # Anti‑doublon
    doublon = (
        supabase.table("preinscriptions")
        .select("*")
        .eq("email", email)
        .eq("seance_id", choix_seance["id"])
        .execute()
        .data
    )

    if doublon:
        st.warning("Vous avez déjà une préinscription pour cette séance.")
        st.stop()

    # Enregistrement
    supabase.table("preinscriptions").insert({
        "type": "exterieur",
        "statut": "en_attente",
        "nom": nom,
        "prenom": prenom,
        "email": email,
        "telephone": telephone,
        "chien_nom": chien_nom,
        "chien_race": chien_race,
        "cours_id": choix_cours["id"],
        "seance_id": choix_seance["id"]
    }).execute()

    st.success("Votre préinscription a bien été enregistrée !")
    st.info("""
Un moniteur confirmera votre présence à votre arrivée au club.
Merci pour votre intérêt et à très bientôt 🐾
""")
