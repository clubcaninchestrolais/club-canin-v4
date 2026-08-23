import streamlit as st

st.sidebar.markdown("## 🐶 Menu Club Canin")

st.sidebar.page_link("pages/Accueil.py", label="🏠 Accueil")
st.sidebar.page_link("pages/Membres.py", label="👥 Membres")
st.sidebar.page_link("pages/Chiens.py", label="🐶 Chiens")
st.sidebar.page_link("pages/Cours.py", label="📅 Cours")
st.sidebar.page_link("pages/Activites_speciales.py", label="🎉 Activités")
st.sidebar.page_link("pages/Presences.py", label="✔️ Présences")

st.sidebar.markdown("---")

st.sidebar.page_link("pages/Archives_membres.py", label="📁 Archives membres")
st.sidebar.page_link("pages/Archives_chiens.py", label="📁 Archives chiens")

st.sidebar.markdown("---")

st.sidebar.page_link("pages/Public.py", label="🌐 Public")
st.sidebar.page_link("pages/Preinscription.py", label="📝 Préinscription extérieure")
