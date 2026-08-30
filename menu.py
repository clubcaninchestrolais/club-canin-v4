import streamlit as st
from supabase_rest import supabase

def hide_streamlit_menu():
    css = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def afficher_notifications():
    """Affiche les notifications actives selon le rôle."""
    role = st.session_state.get("role", "user")

    try:
        notifs = (
            supabase.table("notifications")
            .select("*")
            .eq("actif", True)
            .execute()
            .data
        )
    except Exception:
        return

    for n in notifs:
        if n["role"] in ["all", role]:
            st.sidebar.info(f"📢 {n['titre']} — {n['message']}")


def menu_lateral():
    role = st.session_state.get("role", "user")

    st.sidebar.markdown("## 🐶 Menu Club Canin")

    # --- Notifications internes ---
    afficher_notifications()

    # --- Raccourcis rapides ---
    col1, col2, col3, col4 = st.sidebar.columns(4)

    with col1:
        st.page_link("pages/01_Membres.py", label="👥")

    with col2:
        st.page_link("pages/02_Chiens.py", label="🐶")

    with col3:
        if role == "admin":
            st.page_link("pages/04_Cours.py", label="📘")
        else:
            st.write("")

    with col4:
        st.page_link("pages/20_Cotisations.py", label="💰")

    st.sidebar.markdown("---")

    # --- Gestion du club ---
    st.sidebar.page_link("pages/01_Membres.py", label="👥 Membres")
    st.sidebar.page_link("pages/02_Chiens.py", label="🐶 Chiens")
    st.sidebar.page_link("pages/03_Membres_archives.py", label="📁 Membres archivés")
    st.sidebar.page_link("pages/04_Chiens_archives.py", label="📁 Chiens archivés")
    st.sidebar.page_link("pages/06_Ajouter_Seance.py", label="➕ Ajouter une séance")

    # --- Cours & Séances ---
    if role == "admin":
        st.sidebar.page_link("pages/04_Cours.py", label="📘 Cours")

    st.sidebar.page_link("pages/10_Cours_du_jour.py", label="📅 Cours du jour")
    st.sidebar.page_link("pages/70_Validation_presences.py", label="🟢 Validation des présences")
    st.sidebar.page_link("pages/33_presence_du_jour.py", label="👣 Présences du jour")

    # --- Finances ---
    st.sidebar.markdown("### 💰 Finances")
    st.sidebar.page_link("pages/20_Cotisations.py", label="💳 Cotisations")
    st.sidebar.page_link("pages/21_Abonnements.py", label="🎫 Abonnements")

    if role == "admin":
        st.sidebar.page_link("pages/21_Recettes.py", label="📈 Recettes")
        st.sidebar.page_link("pages/23_Depenses.py", label="🧾 Dépenses")
        st.sidebar.page_link("pages/09_Finances.py", label="💼 Finances globales")

    # --- Flux extérieurs ---
    st.sidebar.markdown("### 🔄 Flux")
    st.sidebar.page_link("pages/50_Inscription_En_Ligne.py", label="🌐 Préinscription publique")

    if role == "admin":
        st.sidebar.page_link("pages/60_Validation_preinscription.py", label="📝 Validation préinscription")

    st.sidebar.page_link("pages/61_Listeexterieurs.py", label="📋 Listing extérieurs")
    st.sidebar.page_link("pages/62_Transformation_exterieur.py", label="🔁 Transformation extérieur → membre")

    # --- Organisations ---
    st.sidebar.markdown("### 🏛️ Organisations")
    st.sidebar.page_link("pages/organisations.py", label="🏛️ Organisations")
    st.sidebar.page_link("pages/95_PV_Reunions.py", label="📄 PV des réunions")


    # --- Technique ---
    st.sidebar.markdown("### ⚙️ Technique")

    if role == "admin":
        st.sidebar.page_link("pages/10_Parametres.py", label="⚙️ Paramètres")

    st.sidebar.page_link("pages/11_Flux_club.py", label="🔄 Flux du club")
    st.sidebar.page_link("pages/01_Apropos.py", label="ℹ️ À propos")

    # --- Admin uniquement ---
    if role == "admin":
        st.sidebar.page_link("pages/60_Rapport.py", label="📊 Rapport")
        st.sidebar.page_link("pages/90_Notifications.py", label="📢 Notifications")
        st.sidebar.page_link("pages/gestion_utilisateurs.py", label="🔐 Gestion utilisateurs")

    st.sidebar.markdown("---")
