import streamlit as st
from supabase import create_client, Client
import datetime

# Sécurité : accès réservé aux membres connectés
if "membre_id" not in st.session_state:
    st.error("Accès réservé aux membres du club.")
    st.stop()

# Connexion Supabase
url = st.secrets["supabase_url"]
key = st.secrets["supabase_key"]
supabase: Client = create_client(url, key)

st.title("🌟 Inscriptions aux activités spéciales du club")

st.write("Les activités ci-dessous sont réservées aux membres du club canin.")

# Charger les activités actives
activites = supabase.table("activites_speciales") \
    .select("*") \
    .eq("actif", True) \
    .order("date", desc=False) \
    .execute().data

if not activites:
    st.info("Aucune activité spéciale n'est actuellement ouverte.")
    st.stop()

# Affichage des activités
for act in activites:
    st.subheader(f"📌 {act['titre']}")
    st.write(f"🗓️ Date : {act['date']}")
    st.write(f"📍 Lieu : {act.get('lieu', 'Non spécifié')}")
    st.write(f"ℹ️ {act.get('description', '')}")

    # Formulaire d'inscription
    with st.form(key=f"form_{act['id']}"):
        st.write("### Inscription")
        nombre = st.number_input("Nombre de participants", min_value=1, value=1)

        submit = st.form_submit_button("S'inscrire à cette activité")

        if submit:
            data = {
                "activite_id": act["id"],
                "membre_id": st.session_state["membre_id"],
                "nombre": nombre,
                "date_inscription": datetime.datetime.now().isoformat(),
                "statut": "inscrit"
            }

            supabase.table("inscriptions_speciales").insert(data).execute()

            st.success("Votre inscription a été enregistrée avec succès !")
            st.experimental_rerun()
