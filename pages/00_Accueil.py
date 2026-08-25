import streamlit as st

st.set_page_config(page_title="Accueil", page_icon="🏠")

st.title("🐾 Club Canin – Accueil")
st.write("Choisissez une section :")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div style='font-size:60px; text-align:center;'>👥</div>", unsafe_allow_html=True)
    st.page_link("pages/01_Membres.py", label="Membres")

with col2:
    st.markdown("<div style='font-size:60px; text-align:center;'>🐶</div>", unsafe_allow_html=True)
    st.page_link("pages/02_Chiens.py", label="Chiens")

with col3:
    st.markdown("<div style='font-size:60px; text-align:center;'>📘</div>", unsafe_allow_html=True)
    st.page_link("pages/04_Cours.py", label="Cours")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("<div style='font-size:60px; text-align:center;'>💰</div>", unsafe_allow_html=True)
    st.page_link("pages/20_Cotisations.py", label="Finances")

with col5:
    st.markdown("<div style='font-size:60px; text-align:center;'>👣</div>", unsafe_allow_html=True)
    st.page_link("pages/33_presence_du_jour.py", label="Présences")

with col6:
    st.markdown("<div style='font-size:60px; text-align:center;'>🌐</div>", unsafe_allow_html=True)
    st.page_link("pages/50_Inscription_En_Ligne.py", label="Public")

st.markdown("---")

st.markdown("<div style='font-size:60px; text-align:center;'>⚙️</div>", unsafe_allow_html=True)
st.page_link("pages/10_Parametres.py", label="Technique")
