import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase
from datetime import date
from menu import hide_streamlit_menu, menu_lateral   # <-- AJOUT

st.set_page_config(page_title="Modifier une séance", page_icon="✏️")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()   # <-- AJOUT

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()          # <-- AJOUT

st.title("✏️ Modifier une séance")

# Vérifier que la séance est bien sélectionnée
seance_id = st.session_state.get("seance_id")

if not seance_id:
    st.error("Aucune séance sélectionnée.")
    st.stop()

# Charger la séance
seance = (
    supabase.table("cours_seances")
    .select("*")
    .eq("id", seance_id)
    .execute()
    .data[0]
)

# Charger le cours lié
cours = (
    supabase.table("cours")
    .select("*")
    .eq("id", seance["cours_id"])
    .execute()
    .data[0]
)

st.subheader(f"Séance du cours : {cours['nom']}")
st.markdown("---")

# Formulaire
date_seance = st.date_input("📅 Date de la séance", value=None)
heure_debut = st.time_input("🕒 Heure de début", value=None)
heure_fin = st.time_input("🕒 Heure de fin", value=None)
actif = st.checkbox("Séance active", value=seance["actif"])

# Pré-remplissage manuel
if "prefill_done" not in st.session_state:
    st.session_state["prefill_done"] = True
    st.session_state["date_seance"] = seance["date_seance"]
    

# Boutons
col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Enregistrer les modifications"):
        data = {
            "date_seance": str(date_seance),
            "heure_debut": str(heure_debut),
            "heure_fin": str(heure_fin),
            "actif": actif
        }

        supabase.table("cours_seances").update(data).eq("id", seance_id).execute()
        st.success("Séance mise à jour avec succès.")
        st.rerun()

with col2:
    if st.button("⬅️ Retour aux séances"):
        st.switch_page("pages/07_Seances_Cours.py")

