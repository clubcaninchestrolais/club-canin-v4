import streamlit as st

st.set_page_config(page_title="Club Canin", page_icon="🐶")

st.title("🐶 Club Canin – Tableau de bord")

st.markdown("### Choisissez une section")

col1, col2 = st.columns(2)

with col1:
    if st.button("👥 Gestion des membres"):
        st.session_state["page"] = "membres"

    if st.button("🐶 Gestion des chiens"):
        st.session_state["page"] = "chiens"

    if st.button("📅 Cours & inscriptions"):
        st.session_state["page"] = "cours"

with col2:
    if st.button("🎉 Activités spéciales"):
        st.session_state["page"] = "activites"

    if st.button("✔️ Présences"):
        st.session_state["page"] = "presences"

    if st.button("📊 Statistiques"):
        st.session_state["page"] = "stats"

st.markdown("---")
st.info("Bienvenue dans le tableau de bord du Club Canin.")
