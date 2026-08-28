import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase
from datetime import date
from menu import hide_streamlit_menu, menu_lateral

st.set_page_config(page_title="Cours du jour", page_icon="📅")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("📅 Cours du jour")

# ---------------------------------------------------------
# 1. Trouver les séances actives FUTURES (requête simple)
# ---------------------------------------------------------

today = date.today().isoformat()

seances_raw = (
    supabase.table("cours_seances")
    .select("*")
    .eq("actif", True)
    .order("date_seance", desc=False)
    .execute()
    .data
)

# ---------------------------------------------------------
# 2. Filtrer côté Python (compatible supabase_rest)
# ---------------------------------------------------------

seances = [
    s for s in seances_raw
    if s["date_seance"]                     # pas vide
    and isinstance(s["date_seance"], str)   # format string
    and len(s["date_seance"]) == 10         # format YYYY-MM-DD
    and s["date_seance"] >= today           # future ou aujourd'hui
]

if not seances:
    st.warning("Aucune séance future active trouvée.")
    st.stop()

# Prendre la première séance future
seance = seances[0]

st.subheader(f"Séance du {seance['date_seance']}")

# ---------------------------------------------------------
# 3. Charger le cours lié à cette séance
# ---------------------------------------------------------
cours = (
    supabase.table("cours")
    .select("*")
    .eq("id", seance["cours_id"])
    .execute()
    .data
)

