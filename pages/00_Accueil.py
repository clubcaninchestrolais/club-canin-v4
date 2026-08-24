import streamlit as st

st.set_page_config(page_title="Accueil", page_icon="🏠")

st.title("🐾 Club Canin – Accueil")
st.write("Choisissez une section :")

# Style pour agrandir les icônes
icone_style = """
<div style='font-size: 48px; text-align: center;'>
    {icone}
</div>
<div style='text-align: center; font-size: 18px; margin-top: -10px;'>
    {label}
</div>
"""

# --- Grille d'icônes cliquables ---
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/01_Membres.py", label=icone_style.format(icone="👥", label="Membres"), unsafe_allow_html=True)

with col2:
    st.page_link("pages/02_Chiens.py", label=icone_style.format(icone="🐶", label="Chiens"), unsafe_allow_html=True)

with col3:
    st.page_link("pages/04_Cours.py", label=icone_style.format(icone="📘", label="Cours"), unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.page_link("pages/20_Cotisations.py", label=icone_style.format(icone="💰", label="Finances"), unsafe_allow_html=True)

with col5:
    st.page_link("pages/33_presence_du_jour.py", label=icone_style.format(icone="👣", label
