import streamlit as st

def securite_user():
    """Sécurité de base : utilisateur connecté obligatoire."""
    if "connected" not in st.session_state or not st.session_state["connected"]:
        st.switch_page("pages/login.py")

def securite_admin():
    """Sécurité admin : connecté + rôle admin obligatoire."""
    securite_user()  # vérifie déjà la connexion

    if st.session_state.get("role") != "admin":
        st.error("Accès réservé à l'administration.")
        st.stop()
