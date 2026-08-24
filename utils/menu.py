import streamlit as st

def afficher_menu():
    st.sidebar.markdown("## 🐶 Menu Club Canin")

    st.sidebar.page_link("pages/01_Membres.py", label="👥 Membres")
    st.sidebar.page_link("pages/02_Chiens.py", label="🐶 Chiens")
    st.sidebar.page_link("pages/04_Cours.py", label="📘 Cours")
    st.sidebar.page_link("pages/20_Cotisations.py", label="💰 Finances")
    st.sidebar.page_link("pages/33_presence_du_jour.py", label="👣 Présences")
    st.sidebar.page_link("pages/50_Inscription_En_Ligne.py", label="🌐 Public")
    st.sidebar.page_link("pages/10_Parametres.py", label="⚙️ Technique")
