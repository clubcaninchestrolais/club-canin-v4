import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Club Canin Chestrolais", page_icon="🐾", layout="centered")

# --- CSS ANIMATION ---
fade_css = """
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}
.fade-in {
    animation: fadeIn 2s ease-in-out;
}
</style>
"""
st.markdown(fade_css, unsafe_allow_html=True)

# --- SPLASH SCREEN ---
splash = st.empty()

with splash.container():
    st.markdown(
        """
        <div class="fade-in" style="text-align:center; margin-top:120px;">
            <img src="/logo.png" width="300">
            <h1 style="color:#003366; font-size:36px; margin-top:20px;">
                Club Canin Chestrolais
            </h1>
            <p style="color:#555; font-size:20px;">
                Portail interne — Version 2026
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- TEMPS D'AFFICHAGE DU LOGO ---
time.sleep(2)

# --- AFFICHAGE DU LOGIN ---
splash.empty()

st.title("🔐 Connexion")
st.write("Veuillez vous connecter pour accéder au portail interne.")

# Ici tu mets ton module de login habituel :
# login_form()
