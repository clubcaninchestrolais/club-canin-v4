import streamlit as st

st.set_page_config(page_title="Club Canin", page_icon="🐾")

# --- MENU PERSONNALISÉ ---
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

# --- CONTENU DE LA PAGE PRINCIPALE ---
st.title("🐾 Club Canin")
st.write("Bienvenue dans votre application.")
st.write("Utilisez le menu à gauche pour naviguer.")
