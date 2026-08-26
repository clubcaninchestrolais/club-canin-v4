import streamlit as st

def hide_streamlit_menu():
    css = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def menu_lateral():
    st.sidebar.markdown("## 🐶 Menu Club Canin")

    # --- Raccourcis rapides ---
    col1, col2, col3, col4 = st.sidebar.columns(4)

    with col1:
        st.page_link("pages/01_Membres.py", label="👥")

    with col2:
        st.page_link("pages/02_Chiens.py", label="🐶")

    with col3:
        st.page_link("pages/04_Cours.py", label="📘")

    with col4:
        st.page_link("pages/20_Cotisations.py", label="💰")

    st.sidebar.markdown("---")

    # --- Gestion du club ---
    st.sidebar.page_link("pages/01_Membres.py", label="👥 Membres")
    st.sidebar.page_link("pages/02_Chiens.py", label="🐶 Chiens")
    st.sidebar.page_link("pages/03_Membres_archives.py", label="📁 Membres archivés")
    st.sidebar.page_link("pages/04_Chiens_archives.py", label="📁 Chiens archivés")

    # --- Cours & Séances ---
    st.sidebar.page_link("pages/04_Cours.py", label="📘 Cours")
    st.sidebar.page_link("pages/06_Ajouter_Seance.py", label="➕ Ajouter une séance")
    st.sidebar.page_link("pages/07_Seances_Cours.py", label="🗓️ Séances des cours")
    st.sidebar.page_link("pages/10_Cours_du_jour.py", label="📅 Cours du jour")
    st.sidebar.page_link("pages/32_Inscription_Seance.py", label="📝 Inscription séance")
    st.sidebar.page_link("pages/70_Validation_presences.py", label="🟢 Validation des présences")  # <-- corrigé
    st.sidebar.page_link("pages/33_presence_du_jour.py", label="👣 Présences du jour")
    st.sidebar.page_link("pages/08_Modifier_Seance.py", label="✏️ Modifier séance")

    st.sidebar.markdown("### 💰 Finances")
    st.sidebar.page_link("pages/20_Cotisations.py", label="💳 Cotisations")
    st.sidebar.page_link("pages/21_Abonnements.py", label="🎫 Abonnements")
    st.sidebar.page_link("pages/21_Recettes.py", label="📈 Recettes")
    st.sidebar.page_link("pages/23_Depenses.py", label="🧾 Dépenses")
    st.sidebar.page_link("pages/09_Finances.py", label="💼 Finances globales")

    st.sidebar.markdown("### 🔄 Flux")
    st.sidebar.page_link("pages/50_Inscription_En_Ligne.py", label="🌐 Préinscription publique")
    st.sidebar.page_link("pages/60_Validation_preinscription.py", label="📝 Validation préinscription")
    st.sidebar.page_link("pages/61_Listeexterieurs.py", label="📋 listing Préinscriptions extérieures")
    st.sidebar.page_link("pages/62_Transformation_exterieur.py", label="🔁 Transformation extérieur → membre")



    st.sidebar.markdown("### 🏛️ Organisations")
    st.sidebar.page_link("pages/organisations.py", label="🏛️ Organisations")

    st.sidebar.markdown("### ⚙️ Technique")
    st.sidebar.page_link("pages/10_Parametres.py", label="⚙️ Paramètres")
    st.sidebar.page_link("pages/11_Flux_club.py", label="🔄 Flux du club")
    st.sidebar.page_link("pages/01_Apropos.py", label="ℹ️ À propos")

    st.sidebar.markdown("---")
