import streamlit as st

st.set_page_config(page_title="Club Canin", page_icon="🐾")

# --- MENU VERTICAL PERSONNALISÉ ---
with st.sidebar:
    st.title("🐾 Menu Club Canin")

    # -------------------------------
    # SECTION : PREINSCRIPTIONS
    # -------------------------------
    st.markdown("### 📝 Préinscriptions")

    st.page_link("pages/50_Inscription_En_Ligne.py", label="Préinscription membre")
    st.page_link("pages/60_Validation_preinscription.py", label="Préinscriptions à valider")

    # Lien vers la préinscription extérieure (page publique)
    st.markdown(
        """
        <a href="http://localhost:8502" target="_blank" style="
            display:block;
            padding:8px;
            background-color:#e8f0fe;
            border-radius:6px;
            text-decoration:none;
            color:#1a73e8;
            font-weight:600;
            margin-bottom:10px;
        ">
        🌐 Préinscription extérieure
        </a>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------
    # SECTION : COURS
    # -------------------------------
    st.markdown("### 📚 Cours")
    st.page_link("pages/10_Cours_du_jour.py", label="Cours du jour")
    st.page_link("pages/04_Cours.py", label="Liste des cours")
    st.page_link("pages/05_Ajouter_Cours.py", label="Ajouter un cours")
    st.page_link("pages/05_Modifier_Cours.py", label="Modifier un cours")
    st.page_link("pages/06_Ajouter_Seance.py", label="Ajouter une séance")
    st.page_link("pages/07_Seances_Cours.py", label="Séances du cours")
    st.page_link("pages/08_Modifier_Seance.py", label="Modifier une séance")
    st.page_link("pages/06_Seances_archivees.py", label="Séances archivées")
    st.page_link("pages/70_Accueil_Cours.py", label="Accueil cours")

    # -------------------------------
    # SECTION : MEMBRES & CHIENS
    # -------------------------------
    st.markdown("### 🐶 Membres & Chiens")
    st.page_link("pages/01_Membres.py", label="Membres")
    st.page_link("pages/01_Ajout_Membre.py", label="Ajouter un membre")
    st.page_link("pages/02_Chiens.py", label="Chiens")
    st.page_link("pages/22_Ajout_Chien.py", label="Ajouter un chien")
    st.page_link("pages/03_Membres_archives.py", label="Membres archivés")
    st.page_link("pages/04_Chiens_archives.py", label="Chiens archivés")
    st.page_link("pages/_fiche_membre_page.py", label="Fiche membre")
    st.page_link("pages/_fiche_chien_page.py", label="Fiche chien")

    # -------------------------------
    # SECTION : FINANCES
    # -------------------------------
    st.markdown("### 💰 Finances")
    st.page_link("pages/20_Cotisations.py", label="Cotisations")
    st.page_link("pages/32_Fiche_Cotisation.py", label="Fiche cotisation")
    st.page_link("pages/21_Abonnements.py", label="Abonnements")
    st.page_link("pages/22_Fiche_Abonnement.py", label="Fiche abonnement")
    st.page_link("pages/21_Recettes.py", label="Recettes")
    st.page_link("pages/22_Fiche_Recette.py", label="Fiche recette")
    st.page_link("pages/23_Depenses.py", label="Dépenses")
    st.page_link("pages/24_Fiche_Depense.py", label="Fiche dépense")
    st.page_link("pages/09_Finances.py", label="Finances générales")

    # -------------------------------
    # SECTION : PRESENCES
    # -------------------------------
    st.markdown("### 📋 Présences")
    st.page_link("pages/31_Choix_Membre_Seance.py", label="Choix membre séance")
    st.page_link("pages/32_Seance_inscription.py", label="Inscription séance")
    st.page_link("pages/33_Seance_presence.py", label="Présences séance")
    st.page_link("pages/40_Historique_Presences.py", label="Historique présences")
    st.page_link("pages/70_Validation_Presences.py", label="Validation présences")
    st.page_link("pages/70_Prepose_Validation.py", label="Préposé validation")

    # -------------------------------
    # SECTION : ADMINISTRATION
    # -------------------------------
    st.markdown("### ⚙️ Administration")
    st.page_link("pages/10_Parametres.py", label="Paramètres")
    st.page_link("pages/11_Flux_club.py", label="Flux du club")
    st.page_link("pages/70_Transformation_membre.py", label="Transformation membre")
    st.page_link("pages/00_Connexion.py", label="Connexion")
    st.page_link("pages/00_Apropos.py", label="À propos")

# --- PAGE D'ACCUEIL ---
st.title("🐾 Club Canin V4")
st.write("Bienvenue dans votre application de gestion du club canin.")
st.write("Utilisez le menu à gauche pour naviguer entre les pages.")
