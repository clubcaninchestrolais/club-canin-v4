import streamlit as st

# 🔒 Sécurité : vérifier la session AVANT tout
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="Rapport", page_icon="📊")

st.title("📊 Rapport")
st.write("Page rapport en construction.")
