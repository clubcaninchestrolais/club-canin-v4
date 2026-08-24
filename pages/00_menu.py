import streamlit as st

st.sidebar.markdown("## 🐶 Menu Club Canin")

# --- ACCUEIL ---
st.sidebar.page_link("pages/Accueil.py", label="🏠 Accueil")

# --- GESTION DU CLUB ---
st.sidebar.markdown("### 👥 Gestion du club")
st.sidebar.page_link("pages/01_Membres.py", label="Membres")
st.sidebar.page_link("pages/01_Ajout_Membre.py", label="Ajouter un membre")
st.sidebar.page_link("pages/03_Membres_archives.py", label="Archives membres")

st.sidebar.page_link("pages/02_Chiens.py", label="Chiens")
st.sidebar.page_link("pages/22_Ajout_Chien.py", label="Ajouter un chien")
st.sidebar.page_link("pages/04_Chiens_archives.py", label="Archives chiens")
#st.sidebar.page_link("pages/23_Fiche_Chien.py", label="Fiche chien")

st.sidebar.page_link("pages/organisations.py", label="Activités")

# --- COURS ---
st.sidebar.markdown("### 📘 Cours")
st.sidebar.page_link("pages/04_Cours.py", label="Cours")
st.sidebar.page_link("pages/05_Ajouter_cours.py", label="Ajouter un cours")
st.sidebar.page_link("pages/05_Modifier_Cours.py", label="Modifier un cours")
st.sidebar.page_link("pages/06_Ajouter_Seance.py", label="Ajouter une séance")
st.sidebar.page_link("pages/06_Seances_archives.py", label="Archives séances")
st.sidebar.page_link("pages/07_Seances_Cours.py", label="Séances des cours")
st.sidebar.page_link("pages/08_Modifier_Seance.py", label="Modifier une séance")
st.sidebar.page_link("pages/10_Cours_du_jour.py", label="Cours du jour")

# --- FINANCES ---
st.sidebar.markdown("### 💰 Finances")
st.sidebar.page_link("pages/20_Cotisations.py", label="Cotisations")
st.sidebar.page_link("pages/21_Abonnements.py", label="Abonnements")
st.sidebar.page_link("pages/21_Recettes.py", label="Recettes")
st.sidebar.page_link("pages/23_Depenses.py", label="Dépenses")
st.sidebar.page_link("pages/24_Fiche_Depense.py", label="Fiche dépense")
st.sidebar.page_link("pages/09_Finances.py", label="Finances")

# --- PRÉSENCES ---
st.sidebar.markdown("### 👣 Présences")
st.sidebar.page_link("pages/33_presence_du_jour.py", label="Présence du jour")
st.sidebar.page_link("pages/40_presences_historiques.py", label="Historique des présences")
st.sidebar.page_link("pages/70_validation_presences.py", label="Validation présences")

# --- PUBLIC ---
st.sidebar.markdown("### 🌐 Public")
st.sidebar.page_link("pages/50_Inscription_En_Ligne.py", label="Inscription en ligne")
st.sidebar.page_link("pages/52_Preinscription_Exterieur.py", label="Préinscription extérieur")
st.sidebar.page_link("pages/60_Validation_préinscription.py", label="Validation préinscription")

# --- TECHNIQUE ---
st.sidebar.markdown("### ⚙️ Technique")
st.sidebar.page_link("pages/10_Paramètres.py", label="Paramètres")
st.sidebar.page_link("pages/11_Flux_club.py", label="Flux club")
st.sidebar.page_link("pages/00_Apropos.py", label="À propos")
st.sidebar.page_link("pages/14_Deconnexion.py", label="Déconnexion")
