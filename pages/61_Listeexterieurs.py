import streamlit as st
from supabase import create_client, Client
from menu import hide_streamlit_menu, menu_lateral
import datetime

# --- Masquer le menu Streamlit + afficher ton menu latéral ---
hide_streamlit_menu()
menu_lateral()

# --- Connexion Supabase ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("📋 Liste des préinscriptions extérieures")

# --- Charger toutes les préinscriptions extérieures ---
preins = (
    supabase.table("preinscriptions")
    .select("*")
    .eq("type", "exterieur")
    .order("date_seance")
    .execute()
    .data
)

if not preins:
    st.info("Aucune préinscription extérieure enregistrée.")
    st.stop()

# --- Filtre par séance ---
dates = sorted({p["date_seance"] for p in preins})
date_choisie = st.selectbox("Filtrer par date de séance :", dates)

preins_filtrees = [p for p in preins if p["date_seance"] == date_choisie]

st.subheader(f"Préinscriptions pour la séance du {date_choisie}")

# --- Affichage compact et propre ---
for p in preins_filtrees:
    st.markdown(f"""
    **{p['prenom']} {p['nom']}**

    • Chien : {p['chien_nom']} ({p['chien_race']})  
    • Email : {p['email']}  
    • Téléphone : {p['telephone']}  
    • Heure : {p['heure_debut']}  
    • Statut : `{p['statut']}`  

    ---
    """)
