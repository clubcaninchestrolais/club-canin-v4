import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Ajouter un chien", page_icon="🐶")

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("🐶 Ajouter un chien")

# ---------------------------------------------------------
# Vérifier membre sélectionné
# ---------------------------------------------------------
membre_id = st.session_state.get("membre_id")

# ---------------------------------------------------------
# Formulaire complet
# ---------------------------------------------------------
with st.form("form_chien"):

    st.subheader("Informations générales")
    nom = st.text_input("Nom du chien")
    race = st.text_input("Race")
    sexe = st.selectbox("Sexe", ["Mâle", "Femelle", "Inconnu"])
    date_naissance = st.date_input("Date de naissance")

    st.subheader("Identification")
    numero_puce = st.text_input("Numéro de puce")
    identification = st.text_input("Identification")
    numero_carnet = st.text_input("Numéro carnet")

    st.subheader("Santé")
    vaccins = st.text_input("Vaccins")
    date_vaccin = st.date_input("Date du dernier vaccin")

    st.subheader("Activité & remarques")
    activite = st.text_input("Activité")
    remarques = st.text_area("Remarques")

    st.subheader("Photo")
    photo_url = st.text_input("URL de la photo")

    submit = st.form_submit_button("Ajouter le chien")

    if submit:
        supabase.table("chiens").insert({
            "nom": nom,
            "race": race,
            "sexe": sexe,
            "date_naissance": str(date_naissance),
            "numero_puce": numero_puce,
            "identification": identification,
            "numero_carnet": numero_carnet,
            "vaccins": vaccins,
            "date_vaccin": str(date_vaccin),
            "activite": activite,
            "remarques": remarques,
            "photo_url": photo_url,
            "id_membre": membre_id,
            "archive": False
        }).execute()

        st.success("🐶 Chien ajouté avec succès !")

        # Si on vient de la fiche membre → retour fiche membre
        if membre_id:
            st.switch_page("pages/21_Fiche_Membre.py")
        else:
            # Sinon → retour à la liste des chiens
            st.switch_page("pages/02_Chiens.py")
