import streamlit as st
import time
from menu import hide_streamlit_menu, menu_lateral

# ---------------------------------------------------------
# 🔐 SÉCURITÉ : accès réservé aux utilisateurs connectés
# ---------------------------------------------------------
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

# --- CONFIGURATION ---
st.set_page_config(page_title="Club Canin – Accueil", page_icon="🏠", layout="centered")

# ---------------------------------------------------------
# 🎬 ANIMATION SPLASH SCREEN (post-login)
# ---------------------------------------------------------

# CSS animation
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

# Splash container
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
                Chargement du portail interne...
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Temps d'affichage
time.sleep(2)

# Effacer l'animation
splash.empty()

# ---------------------------------------------------------
# MENU LATERAL + CONTENU
# ---------------------------------------------------------

hide_streamlit_menu()
menu_lateral()

st.title("🐾 Club Canin – Accueil")
st.write("Choisissez une section :")

# --- BLOC CLIQUABLE ---
def bloc(page, icone, texte):
    if st.button(f"{icone}\n{texte}", key=f"btn_{page}"):
        st.switch_page(f"pages/{page}.py")

# ---------------------------------------------------------
# 👥 MEMBRES & CHIENS
# ---------------------------------------------------------
st.subheader("👥 Membres & Chiens")

col1, col2, col3, col4 = st.columns(4)

with col1:
    bloc("01_Membres", "👥", "Membres")

with col2:
    bloc("02_Chiens", "🐶", "Chiens")

with col3:
    bloc("20_Cotisations", "💳", "Cotisations")

with col4:
    bloc("21_Abonnements", "🎫", "Abonnements")

# ---------------------------------------------------------
# 📁 ARCHIVES
# ---------------------------------------------------------
st.subheader("📁 Archives")

colA1, colA2 = st.columns(2)

with colA1:
    bloc("03_Membres_archives", "📁", "Membres archivés")

with colA2:
    bloc("04_Chiens_archives", "📁", "Chiens archivés")

# ---------------------------------------------------------
# 📘 COURS
# ---------------------------------------------------------
st.subheader("📘 Gestion des cours")

col5, col6, col7 = st.columns(3)

with col5:
    bloc("04_Cours", "📘", "Cours")

with col6:
    bloc("07_Seances_Cours", "🗓️", "Séances")

with col7:
    bloc("10_Cours_du_jour", "📅", "Cours du jour")

col8, col9, col10 = st.columns(3)

with col8:
    bloc("08_Modifier_Seance", "✏️", "Modifier séance")

with col9:
    st.write("")

with col10:
    st.write("")

# ---------------------------------------------------------
# 💰 FINANCES
# ---------------------------------------------------------
st.subheader("💰 Finances")

col11, col12, col13, col14 = st.columns(4)

with col11:
    bloc("23_Depenses", "🧾", "Dépenses")

with col12:
    bloc("21_Recettes", "📈", "Recettes")

with col13:
    bloc("09_Finances", "💼", "Finances globales")

with col14:
    bloc("QR_Paiement", "🔲", "QR Paiement")

# ---------------------------------------------------------
# 🔄 FLUX DE VALIDATION
# ---------------------------------------------------------
st.subheader("🔄 Flux de validation")

colV1, colV2, colV3, colV4, colV5, colV6 = st.columns(6)

with colV1:
    bloc("50_Inscription_En_Ligne", "🌐", "Préinscription publique")

with colV2:
    bloc("60_Validation_preinscription", "📝", "Validation préinscription")

with colV3:
    bloc("33_presence_du_jour", "👣", "Présences du jour")

with colV4:
    bloc("70_Validation_presences", "🟢", "Validation des présences")

with colV5:
    bloc("61_Listeexterieurs", "📋", "Préinscriptions extérieures")

with colV6:
    bloc("62_Transformation_exterieur", "🔁", "Transformer extérieur")

# ---------------------------------------------------------
# 🏛️ ORGANISATIONS
# ---------------------------------------------------------
st.subheader("🏛️ Organisations")

bloc("organisations", "🏛️", "Organisations")

# ---------------------------------------------------------
# ⚙️ TECHNIQUE
# ---------------------------------------------------------
st.subheader("⚙️ Technique")

col14, col15, col16 = st.columns(3)

with col14:
    bloc("10_Parametres", "⚙️", "Paramètres")

with col15:
    bloc("11_Flux_club", "🔄", "Flux du club")

with col16:
    bloc("01_Apropos", "ℹ️", "À propos")

st.markdown("---")
