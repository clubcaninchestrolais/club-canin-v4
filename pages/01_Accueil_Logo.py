import streamlit as st
from menu import hide_streamlit_menu, menu_lateral

# Sécurité
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

# Configuration
st.set_page_config(page_title="Accueil – Logo", page_icon="🏠", layout="centered")

hide_streamlit_menu()
menu_lateral()

# --- PAGE ACCUEIL AVEC LOGO ---
st.markdown(
    """
    <div style="text-align:center; margin-top:80px;">
        <img src="logo.png" width="350">
    </div>
    """,
    unsafe_allow_html=True
)
