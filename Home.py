import streamlit as st

st.set_page_config(page_title="Club Canin", page_icon="🐶")

# Masquer le menu Streamlit
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

st.title("🐶 Club Canin – Tableau de bord")
st.markdown("### Choisissez une section")

# Mise en page en 2 colonnes
col1, col2 = st.columns(2)

with col1:
    if st.button("👥 Gestion des membres"):
        st.switch_page("pages/Membres.py")

    if st.button("🐶 Gestion des chiens"):
        st.switch_page("pages/Chiens.py")

    if st.button("📅 Cours et inscriptions"):
        st.switch_page("pages/Cours.py")

with col2:
    if st.button("🎉 Activités spéciales"):
        st.switch_page("pages/Activites_speciales.py")

    if st.button("✔️ Présences"):
        st.switch_page("pages/Presences.py")

    if st.button("📊 Statistiques"):
        st.switch_page("pages/Stats.py")

st.markdown("---")
st.info("Bienvenue dans le tableau de bord du Club Canin.")
