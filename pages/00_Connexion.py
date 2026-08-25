import streamlit as st

st.set_page_config(page_title="Accueil", page_icon="🏠")

st.title("🏠 Accueil")

st.write("Bienvenue dans l'application Club Canin Pro V2")

# -------------------------
# MENU CORRIGÉ
# -------------------------

st.subheader("👤 Membres")
st.page_link("pages/01_Membres.py", label="Liste des membres")
st.page_link("pages/2_Ajout_Membre.py", label="Ajouter un membre")
st.page_link("pages/3_Edit_Membre.py", label="Modifier un membre")
st.page_link("pages/4_Fiche_Membre.py", label="Fiche membre")
st.page_link("pages/7_Membres_Archives.py", label="Archives membres")

st.subheader("🐶 Chiens")
st.page_link("pages/2_Chiens.py", label="Liste des chiens")
st.page_link("pages/5_Ajout_Chien.py", label="Ajouter un chien")
st.page_link("pages/4_Edit_Chien.py", label="Modifier un chien")
st.page_link("pages/23_Fiche_Chien.py", label="Fiche chien")
st.page_link("pages/6_Chiens_Archives.py", label="Archives chiens")

st.subheader("📘 Cours")
st.page_link("pages/4_Cours.py", label="Cours")
st.page_link("pages/31_inscription_membre_cours.py", label="Inscription membre cours")
st.page_link("pages/32_participants_cours.py", label="Participants cours")
st.page_link("pages/33_validation_presences.py", label="Validation présences")
st.page_link("pages/36_presences_par_cours.py", label="Présences par cours")
st.page_link("pages/37_presences_par_membre.py", label="Présences par membre")
st.page_link("pages/38_historique_presences.py", label="Historique présences")

st.subheader("📊 Statistiques")
st.page_link("pages/39_statistiques_mensuelles.py", label="Statistiques mensuelles")
st.page_link("pages/40_statistiques_annuelles.py", label="Statistiques annuelles")
st.page_link("pages/7_Statistiques.py", label="Statistiques générales")

st.subheader("💰 Finances")
st.page_link("pages/5_Cotisations.py", label="Cotisations")
st.page_link("pages/6_Finances.py", label="Finances")
st.page_link("pages/9_Finances_Annuelles.py", label="Finances annuelles")
st.page_link("pages/7_recettes.py", label="Recettes")
st.page_link("pages/8_dépenses.py", label="Dépenses")
st.page_link("pages/10_ClotureFinances.py", label="Clôture finances")

st.subheader("⚙️ Technique")
st.page_link("pages/8_Parametres.py", label="Paramètres")
st.page_link("pages/15_flux.py", label="Flux")
st.page_link("pages/13_A_Propos.py", label="À propos")
st.page_link("pages/14_Deconnexion.py", label="Déconnexion")
