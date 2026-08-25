import streamlit as st

st.set_page_config(page_title="Accueil", page_icon="🏠")

st.title("🐾 Club Canin – Accueil")
st.write("Choisissez une section :")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/01_Membres.py", label="👥👥\nMembres")

with col2:
    st.page_link("pages/02_Chiens.py", label="🐶🐶\nChiens")

with col3:
    st.page_link("pages/04_Cours.py", label="📘📘\nCours")

col4, col5, col6 = st.columns(3)

with col4:
    st.page_link("pages/20_Cotisations.py", label="💰💰\nFinances")

with col5:
    st.page_link("pages/33_presence_du_jour.py", label="👣👣\nPrésences")

with col6:
    st.page_link("pages/50_Inscription_En_Ligne.py", label="🌐🌐\nPublic")

st.markdown("---")

st.page_link("pages/10_Parametres.py", label="⚙️⚙️\nTechnique")
