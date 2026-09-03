import streamlit as st
from securite import securite_admin
securite_admin()

from datetime import datetime, date
from supabase_rest import supabase, log_action
from menu import hide_streamlit_menu, menu_lateral


st.set_page_config(page_title="Finances", page_icon="💰")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("Résumé financier du club")

# -----------------------------
# Choix de l'année
# -----------------------------
annee = st.selectbox(
    "Choisir l'année",
    list(range(2020, datetime.now().year + 1)),
    index=(datetime.now().year - 2020)
)

# -----------------------------
# Chargement des données
# -----------------------------
recettes = (
    supabase.table("recettes")
    .select("*")
    .execute()
    .data
)

depenses = (
    supabase.table("depenses")
    .select("*")
    .execute()
    .data
)

# -----------------------------
# Filtre par année
# -----------------------------
recettes_annee = [
    r for r in recettes
    if str(r.get("date", "")).startswith(str(annee))
]

depenses_annee = [
    d for d in depenses
    if str(d.get("date", "")).startswith(str(annee))
]

# -----------------------------
# Totaux sécurisés
# -----------------------------
total_recettes = sum(float(r.get("montant") or 0) for r in recettes_annee)
total_depenses = sum(float(d.get("montant") or 0) for d in depenses_annee)
resultat = total_recettes
