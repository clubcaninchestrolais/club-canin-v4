import streamlit as st
from menu import hide_streamlit_menu, menu_lateral

# --- CONFIGURATION ---
st.set_page_config(page_title="Club Canin – Accueil", page_icon="🏠")

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
    bloc("11_Flux_club", "🔄", "Flux du club")

with col9:
    bloc("08_Modifier_Seance", "✏️", "Modifier séance")  # interne

with col10:
    st.write("")

# ---------------------------------------------------------
# 💰 FINANCES (optionnel)
# ---------------------------------------------------------
st.subheader("💰 Finances")

col11, col12, col13 = st.columns(3)

with col11:
    bloc("23_Recettes", "📈", "Recettes")

with col12:
    bloc("09_Finances", "💼", "Finances globales")

with col13:
    st.write("")

# ---------------------------------------------------------
# 👣 PRESENCES
# ---------------------------------------------------------
st.subheader("👣 Présences")
bloc("33_presence_du_jour", "👣", "Présences du jour")

# ---------------------------------------------------------
# 🌐 PUBLIC
# ---------------------------------------------------------
st.subheader("🌐 Public")
bloc("50_Inscription_En_Ligne", "🌐", "Inscription en ligne")

# ---------------------------------------------------------
# ⚙️ TECHNIQUE
# ---------------------------------------------------------
st.subheader("⚙️ Technique")
bloc("10_Parametres", "⚙️", "Paramètres")

st.markdown("---")
st.write("Bienvenue dans votre tableau de bord du Club Canin 🐾")
