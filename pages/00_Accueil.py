import streamlit as st

st.set_page_config(page_title="Accueil", page_icon="🏠")

st.title("🐾 Club Canin – Accueil")
st.write("Choisissez une section :")

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
