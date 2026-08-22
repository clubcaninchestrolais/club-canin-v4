import streamlit as st

st.title("🐶 Accueil du Club Canin")

st.markdown("### Accès rapide")

if st.button("👥 Membres"):
    st.switch_page("pages/Membres.py")

if st.button("🐶 Chiens"):
    st.switch_page("pages/Chiens.py")

if st.button("📅 Cours"):
    st.switch_page("pages/Cours.py")

if st.button("🎉 Activités spéciales"):
    st.switch_page("pages/Activites_speciales.py")

if st.button("✔️ Présences"):
    st.switch_page("pages/Presences.py")

if st.button("📁 Archives"):
    st.switch_page("pages/Archives.py")

if st.button("🌐 Préinscription extérieure"):
    st.switch_page("pages/Public.py")
