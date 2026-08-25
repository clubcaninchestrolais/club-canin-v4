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

    col1, col2, col3, col4 = st.sidebar.columns(4)

    with col1:
        st.page_link("pages/01_Membres.py", label="👥")

    with col2:
        st.page_link("pages/02_Chiens.py", label="🐶")

    with col3:
        st.page_link("pages/04_Cours.py", label="📘")

    with col4:
        st.page_link("pages/20_Cotisations.py", label="💰")

    st.sidebar.page_link("pages/01_Membres.py", label="👥 Membres")
    st.sidebar.page_link("pages/02_Chiens.py", label="🐶 Chiens")
    st.sidebar.page_link("pages/04_Cours.py", label="📘 Cours")
    st.sidebar.page_link("pages/20_Cotisations.py", label="💰 Cotisations")
    st.sidebar.page_link("pages/33_presence_du_jour.py", label="👣 Présences")
    st.sidebar.page_link("pages/50_Inscription_En_Ligne.py", label="🌐 Public")
    st.sidebar.page_link("pages/10_Parametres.py", label="⚙️ Technique")
