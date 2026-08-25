import streamlit as st
from menu import hide_streamlit_menu, menu_lateral

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Club Canin – Accueil", page_icon="🏠")

# --- MASQUER LE MENU AUTOMATIQUE DE STREAMLIT ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

# --- TITRE ---
st.title("🐾 Club Canin – Accueil")
st.write("Choisissez une section :")

# --- PARAMÈTRES DES BLOCS ---
ICON_SIZE = 70
TEXT_SIZE = 22

def bloc(page, icone, texte):
    """
    Bloc cliquable : icône + texte
    Utilise un bouton invisible pour une navigation Streamlit propre.
    """
    if st.button(f"{icone}\n{texte}", key=f"btn_{page}", help=f"Ouvrir {texte}"):
        st.switch_page(f"pages/{page}.py")

# --- TABLEAU DE BORD ---
col1, col2, col3 = st.columns(3)

with col1:
    bloc("01_Membres", "👥", "Membres")

with col2:
    bloc("02_Chiens", "🐶", "Chiens")

with col3:
    bloc("04_Cours", "📘", "Cours")

col4, col5, col6 = st.columns(3)

with col4:
    bloc("20_Cotisations", "💰", "Finances")

with col5:
    bloc("33_presence_du_jour", "👣", "Présences")

with col6:
    bloc("50_Inscription_En_Ligne", "🌐", "Public")

st.markdown("---")

bloc("10_Parametres", "⚙️", "Technique")
