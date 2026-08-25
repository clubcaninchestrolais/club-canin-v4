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

# --- BLOC CLIQUABLE AVEC ICÔNE AGRANDIE ---
def bloc(page, icone, texte):
    # Style CSS pour agrandir l’icône et le texte
    st.markdown(
        f"""
        <style>
        .btn_{page} {{
            font-size: 70px;
            padding: 10px;
            background: none;
            border: none;
            cursor: pointer;
            text-align: center;
        }}
        .txt_{page} {{
            font-size: 24px;
            text-align: center;
            margin-top: -10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Bouton invisible mais cliquable
    if st.button(f"{icone}", key=f"btn_{page}", help=f"Ouvrir {texte}"):
        st.switch_page(f"pages/{page}.py")

    # Texte sous l’icône
    st.markdown(f"<div class='txt_{page}'>{texte}</div>", unsafe_allow_html=True)


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
    bloc("20_Cotisations",
