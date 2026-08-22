iimport streamlit as st

st.title("🐶 Accueil du Club Canin")

col1, col2 = st.columns(2)

with col1:
    if st.button("👥 Membres"):
        st.switch_page("pages/Membres.py")

    if st.button("🐶 Chiens"):
        st.switch_page("pages/Chiens.py")

    if st.button("📅 Cours"):
        st.switch_page("pages/Cours.py")

with col2:
    if st.button("🎉 Activités"):
        st.switch_page("pages/Activites_speciales.py")

    if st.button("✔️ Présences"):
        st.switch_page("pages/Presences.py")

    if st.button("📁 Archives"):
        st.switch_page("pages/Archives.py")
