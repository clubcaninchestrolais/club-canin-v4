import streamlit as st
from supabase import create_client, Client
from menu import hide_streamlit_menu, menu_lateral
import datetime

# 🔒 Sécurité : vérifier la session AVANT tout
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

hide_streamlit_menu()
menu_lateral()

# --- Connexion Supabase ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("📝 Inscription à une séance")

# --- Charger les séances ---
seances = (
    supabase.table("cours_seances")
    .select("*")
    .order("date_seance")
    .execute()
    .data
)

if not seances:
    st.info("Aucune séance disponible.")
    st.stop()

# --- Choix de la séance ---
choix_seance = st.selectbox(
    "Sélectionner une séance",
    options=seances,
    format_func=lambda s: f"{s['date_seance']} – {s['nom_seance']}"
)

seance_id = choix_seance["id"]

# --- Charger les membres ---
membres = (
    supabase.table("membres")
    .select("*")
    .eq("actif", True)
    .order("nom")
    .execute()
    .data
)

if not membres:
    st.info("Aucun membre actif.")
    st.stop()

# --- Choix du membre ---
choix_membre = st.selectbox(
    "Sélectionner un membre",
    options=membres,
    format_func=lambda m: f"{m['prenom']} {m['nom']}"
)

membre_id = choix_membre["id"]

# --- Charger les chiens du membre ---
chiens = (
    supabase.table("chiens")
    .select("*")
    .eq("id_membre", membre_id)
    .execute()
    .data
)

if not chiens:
    st.warning("Ce membre n'a pas de chien enregistré.")
    st.stop()

# --- Choix du chien ---
choix_chien = st.selectbox(
    "Sélectionner un chien",
    options=chiens,
    format_func=lambda c: f"{c['nom']} ({c['race']})"
)

chien_id = choix_chien["id"]

st.markdown("---")

# --- Inscription ---
if st.button("Inscrire à la séance"):

    insertion = supabase.table("cours_presences").insert({
        "membre_id": membre_id,
        "chien_id": chien_id,
        "date_presence": datetime.date.today().isoformat(),
        "seance_id": seance_id,
        "present": True
    }).execute()

    if not insertion.data:
        st.error("❌ Supabase a refusé l'insertion de la présence.")
        st.json(insertion)
        st.stop()

    st.success("✅ Inscription enregistrée.")
    st.rerun()
