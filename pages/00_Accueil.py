import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Club Canin – Accueil", page_icon="🏠")

# --- MENU LATÉRAL ---
st.sidebar.markdown("## 🐶 Menu Club Canin")

# Navigation rapide par icônes
col1, col2, col3, col4 = st.sidebar.columns(4)

with col1:
    st.page_link("pages/01_Membres.py", label="👥")

with col2:
    st.page_link("pages/02_Chiens.py", label="🐶")

with col3:
    st.page_link("pages/04_Cours.py", label="📘")

with col4:
    st.page_link("pages/20_Cotisations.py", label="💰")

# Menu détaillé
st.sidebar.page_link("pages/01_Membres.py", label="👥 Membres")
st.sidebar.page_link("pages/02_Chiens.py", label="🐶 Chiens")
st.sidebar.page_link("pages/04_Cours.py", label="📘 Cours")
st.sidebar.page_link("pages/20_Cotisations.py", label="💰 Finances")
st.sidebar.page_link("pages/33_presence_du_jour.py", label="👣 Présences")
st.sidebar.page_link("pages/50_Inscription_En_Ligne.py", label="🌐 Public")
st.sidebar.page_link("pages/10_Parametres.py", label="⚙️ Technique")

# --- TITRE DE LA PAGE ---
st.title("🐾 Club Canin – Accueil")
st.write("Choisissez une section :")

# --- PARAMÈTRES D'AFFICHAGE DES BLOCS ---
ICON_SIZE = 70
TEXT_SIZE = 22

def bloc(page, icone, texte):
    html = f"""
    <div style='text-align:center;'>
        <a href='?page={page}' style='text-decoration:none; color:inherit;'>
            <div style='font-size:{ICON_SIZE}px;'>{icone}</div>
            <div style='font-size:{TEXT_SIZE}px;'>{texte}</div>
        </a>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

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
