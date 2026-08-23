import streamlit as st

st.sidebar.markdown("## 🐶 Menu Club Canin")

# --- ACCUEIL ---
st.sidebar.page_link("pages/Accueil.py", label="🏠 Accueil")

# --- GESTION DU CLUB ---
st.sidebar.markdown("### 👥 Gestion du club")
st.sidebar.page_link("pages/01_Membres.py", label="Membres")
st.sidebar.page_link("pages/02_Chiens.py", label="Chiens")
st.sidebar.page_link("pages/organisations.py", label="Activités")
st.sidebar.page_link("pages/04_Cours.py", label="Cours")
st.sidebar.page_link("pages/07_Seances_Cours.py", label="Séances des cours")
#st.sidebar.page_link("pages/33_presence_du_jour.py", label="Présence du jour")

# --- FINANCES ---
st.sidebar.markdown("### 💰 Finances")
st.sidebar.page_link("pages/20_Cotisations.py", label="Cotisations")
st.sidebar.page_link("pages/21_Abonnements.py", label="Abonnements")
st.sidebar.page_link("pages/21_Recettes.py", label="Recettes")
st.sidebar.page_link("pages/23_Depenses.py", label="Dépenses")

# --- PUBLIC ---
st.sidebar.markdown("### 🌐 Public")
st.sidebar.page_link("pages/50_Inscription_En_Ligne.py", label="Inscription en ligne")
st.sidebar.page_link("pages/52_Preinscription_Exterieur.py", label="Préinscription extérieure")
st.sidebar.page_link("pages/60_Validation_preinscription.py", label="Validation préinscription")

# --- ADMINISTRATION ---
st.sidebar.markdown("### 🔒 Administration")
#st.sidebar.page_link("pages/40_presences_historiques.py", label="Présences historiques")
st.sidebar.page_link("pages/70_validation_presences.py", label="Validation présences")
st.sidebar.page_link("pages/70_Transformation_membre.py", label="Transformation membre")
st.sidebar.page_link("pages/10_Parametres.py", label="Paramètres")
