import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

st.set_page_config(page_title="Membres archivés", page_icon="🗃️")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("🗃️ Membres archivés")

# Charger uniquement les membres ARCHIVÉS
membres = (
    supabase.table("membres")
    .select("*")
    .eq("archive", True)
    .execute()
    .data
)

st.write("### Membres archivés")

# Style moderne (alternance de lignes)
def ligne_style(index):
    return (
        "background-color: #f7f7f7; padding: 6px; border-radius: 4px;"
        if index % 2 == 0
        else "padding: 6px;"
    )

# En-tête du tableau
header = st.columns([2, 2, 2, 3, 1, 1])
header[0].markdown("**Nom**")
header[1].markdown("**Prénom**")
header[2].markdown("**Téléphone**")
header[3].markdown("**E-mail**")
header[4].markdown("**Actif**")
header[5].markdown("**Fiche**")

st.markdown("---")

# Affichage ligne par ligne
for index, ligne in enumerate(membres):

    prenom = ligne.get("prenom", "")
    nom = ligne.get("nom", "")
    email = ligne.get("email", "")
    telephone = ligne.get("telephone", "")
    actif = "🟢" if ligne.get("actif", True) else "🔴"

    cols = st.columns([2, 2, 2, 3, 1, 1])

    with cols[0]:
        st.markdown(f"<div style='{ligne_style(index)}'>{nom}</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown(f"<div style='{ligne_style(index)}'>{prenom}</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown(f"<div style='{ligne_style(index)}'>📞 {telephone}</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown(f"<div style='{ligne_style(index)}'>📧 {email}</div>", unsafe_allow_html=True)

    with cols[4]:
        st.markdown(f"<div style='{ligne_style(index)}'>{actif}</div>", unsafe_allow_html=True)

    with cols[5]:
        if st.button("🔍", key=f"fiche_arch_{ligne['id']}"):
            st.session_state["membre_id"] = ligne["id"]
            st.switch_page("pages/_fiche_membre_page.py")

st.markdown("---")
