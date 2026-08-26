import streamlit as st
from menu import hide_streamlit_menu, menu_lateral

hide_streamlit_menu()
menu_lateral()

st.set_page_config(page_title="Accueil", page_icon="🏠")

st.title("🏠 Accueil — Club Canin")

st.markdown("### 🎯 Accès rapide aux fonctionnalités principales")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/10_Cours_du_jour.py", label="📅 Cours du jour")
    st.page_link("pages/32_Inscription_Seance.py", label="📝 Inscription séance")

with col2:
    st.page_link("pages/70_Validation_presences.py", label="🟢 Validation des présences")   # <-- AJOUT
    st.page_link("pages/33_presence_du_jour.py", label="👣 Présences du jour")

with col3:
    st.page_link("pages/06_Ajouter_Seance.py", label="➕ Ajouter une séance")
    st.page_link("pages/07_Seances_Cours.py", label="🗓️ Séances des cours")

st.markdown("---")

st.markdown("### 🐶 Gestion du club")
st.page_link("pages/01_Membres.py", label="👥 Membres")
st.page_link("pages/02_Chiens.py", label="🐶 Chiens")
st.page_link("pages/03_Membres_archives.py", label="📁 Membres archivés")
st.page_link("pages/04_Chiens_archives.py", label="📁 Chiens archivés")

st.markdown("---")

st.markdown("### 💰 Finances")
st.page_link("pages/20_Cotisations.py", label="💳 Cotisations")
st.page_link("pages/21_Abonnements.py", label="🎫 Abonnements")
st.page_link("pages/21_Recettes.py", label="📈 Recettes")
st.page_link("pages/23_Depenses.py", label="🧾 Dépenses")
st.page_link("pages/09_Finances.py", label="💼 Finances globales")

st.markdown("---")

st.markdown("### 🌐 Préinscriptions")
st.page_link("pages/50_Inscription_En_Ligne.py", label="🌐 Préinscription publique")
st.page_link("pages/60_Validation_preinscription.py", label="📝 Validation préinscription")

st.markdown("---")

st.markdown("### ⚙️ Technique")
st.page_link("pages/10_Parametres.py", label="⚙️ Paramètres")
st.page_link("pages/11_Flux_club.py", label="🔄 Flux du club")
st.page_link("pages/01_Apropos.py", label="ℹ️ À propos")


