import streamlit as st

st.set_page_config(page_title="Club Canin", page_icon="🐾")

# --- Animation fade-in simple et sûre ---
fade_css = """
<style>
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
.fade-in {
    animation: fadeIn 2s ease-in-out;
}
</style>
"""
st.markdown(fade_css, unsafe_allow_html=True)

st.title("🐾 Club Canin V4")

# --- Logo avec fade-in ---
st.markdown(
    """
    <div class="fade-in" style="text-align:center; margin-top:20px;">
        <img src="https://i.imgur.com/yourlogo.png" width="250">
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Bienvenue dans votre application de gestion du club canin.")
st.write("Pour le public : utilisez le lien d’inscription extérieure.")
st.write("Pour le club : connectez-vous via la page de connexion pour accéder au menu complet.")
