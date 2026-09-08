import streamlit as st
from menu import hide_streamlit_menu, menu_lateral

if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="Accueil – Logo", page_icon="🏠", layout="centered")

hide_streamlit_menu()
menu_lateral()

st.markdown("""
<style>
.logo-zoom {
    transition: transform 0.4s ease-in-out;
}
.logo-zoom:hover {
    transform: scale(1.08);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align:center; margin-top:80px;'>", unsafe_allow_html=True)
st.markdown("<img src='logo.png' width='550' class='logo-zoom'>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
