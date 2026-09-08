import streamlit as st
from menu import hide_streamlit_menu, menu_lateral

# Sécurité
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

# Configuration
st.set_page_config(page_title="Accueil – Logo", page_icon="🏠", layout="centered")

hide_streamlit_menu()
menu_lateral()

# --- PAGE ACCUEIL AVEC LOGO AMÉLIORÉ ---
st.markdown(
    """
    <div style="
        text-align:center; 
        margin-top:60px;
        padding:40px;
        background: linear-gradient(135deg, #f0f4ff, #ffffff);
        border-radius:20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    ">
        <h2 style="color:#003366; margin-bottom:30px;">
            Bienvenue dans le programme du Club Canin Chestrolais
        </h2>
    """,
    unsafe_allow_html=True
)

st.image("logo.png", width=550)

st.markdown("</div>", unsafe_allow_html=True)
