import streamlit as st

st.set_page_config(page_title="Accueil", page_icon="🏠")

st.title("🐾 Club Canin – Accueil")
st.write("Choisissez une section :")

# Taille des icônes et du texte
ICON_SIZE = 70
TEXT_SIZE = 22

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div style='text-align:center; font-size:{ICON_SIZE}px;'>👥</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; font-size:{TEXT_SIZE}px;'>Membres</div>", unsafe_allow_html=True)
    st.page_link("pages/01_Membres.py", label="Ouvrir")

with col2:
    st.markdown(f"<div style='text-align:center; font-size:{ICON_SIZE}px;'>🐶</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; font-size:{TEXT_SIZE}px;'>Chiens</div>", unsafe_allow_html=True)
    st.page_link("pages/02_Chiens.py", label="Ouvrir")

with col3:
    st.markdown(f"<div style='text-align:center; font-size:{ICON_SIZE}px;'>📘</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; font-size:{TEXT_SIZE}px;'>Cours</div>", unsafe_allow_html=True)
    st.page_link("pages/04_Cours.py", label="Ouvrir")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown(f"<div style='text-align:center; font-size:{ICON_SIZE}px;'>💰</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; font-size:{TEXT_SIZE}px;'>Finances</div>", unsafe_allow_html=True)
    st.page_link("pages/20_Cotisations.py", label="Ouvrir")

with col5:
    st.markdown(f"<div style='text-align:center; font-size:{ICON_SIZE}px;'>👣</div>", unsafe_allow_html=True)
    st.markdown
