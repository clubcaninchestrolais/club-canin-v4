import streamlit as st
from menu import hide_streamlit_menu, menu_lateral

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Club Canin – Accueil", page_icon="🏠")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- MENU PERSONNALISÉ ---
menu_lateral()

# --- TITRE ---
st.title("🐾 Club Canin – Accueil")
st.write("Choisissez une section :")

# --- BLOC CLIQUABLE ---
def bloc(page, icone, texte):
    if st.button(f"{icone}\n{texte}", key=f"btn_{page}", help=f"Ouvrir {texte}"):
        st.switch_page(f"pages/{page}.py")

# --- TABLEAU DE BORD COMPLET ---

# Ligne 1 : Gestion du club
col1, col2, col3, col4 = st.columns(4)

with col1:
    bloc("01_Membres", "👥", "Membres")

with col2:
    bloc("02_Chiens", "🐶", "Chiens")

with col3:
    bloc("04_Cours", "📘", "Cours")

with col4:
    bloc("33_presence_du_jour", "👣", "Présences")

# Ligne 2 : Gestion avancée
col5, col6, col7, col8 = st.columns(4)

with col5:
    bloc("40_Activites", "🎉", "Activités")

with col6:
    bloc("41_Moniteurs", "🧑‍🏫", "Moniteurs")

with col7:
    bloc("20_Cotisations", "💰", "Finances")

with col8:
    bloc("70_Abonnements", "📄", "Abonnements")

# Ligne 3 : Administration
col9, col10, col11, col12 = st.columns(4)

with col9:
    bloc("80_Documents", "📁", "Documents")

with col10:
    bloc("90_Stats", "📊", "Statistiques")

with col11:
    bloc("10_Parametres", "⚙️", "Paramètres")

with col12:
    bloc("01_Apropos", "ℹ️", "À propos")

# Ligne 4 : Public
col13, col14 = st.columns(2)

with col13:
    bloc("50_Inscription_En_Ligne", "🌐", "Inscription en ligne")

with col14:
    bloc("51_Preinscription", "📝", "Préinscription extérieure")
