import streamlit as st

st.set_page_config(page_title="Accueil", page_icon="🏠")

st.title("🐾 Club Canin – Accueil")
st.write("Choisissez une section :")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/01_Membres.py",
                 label="<span style='font-size:48px;'>👥</span><br>Membres",
                 unsafe_allow_html=True)

with col2:
    st.page_link("pages/02_Chiens.py",
                 label="<span style='font-size:48px;'>🐶</span><br>Chiens",
                 unsafe_allow_html=True)

with col3:
    st.page_link("pages/04_Cours.py",
                 label="<span style='font-size:48px;'>📘</span><br>Cours",
                 unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.page_link("pages/20_Cotisations.py",
                 label="<span style='font-size:48px;'>💰</span><br>Finances",
                 unsafe_allow_html=True)

with col5:
    st.page_link("pages/33_presence_du_jour.py",
                 label="<span style='font-size:48px;'>👣</span><br>Présences",
                 unsafe_allow_html=True)

with col6:
    st.page_link("pages/50_Inscription_En_Ligne.py",
                 label="<span style='font-size:48px;'>🌐</span><br>Public",
                 unsafe_allow_html=True)

st.markdown("---")

st.page_link("pages/10_Parametres.py",
             label="<span style='font-size:48px;'>⚙️</span><br>Technique",
             unsafe_allow_html=True)
