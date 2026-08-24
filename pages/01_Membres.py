import streamlit as st
from supabase_rest import supabase

# Page en mode large
st.set_page_config(page_title="Membres", page_icon="👥", layout="wide")

st.title("Liste des membres")

# Charger uniquement les membres actifs
membres = (
    supabase.table("membres")
    .select("*")
    .eq("archive", False)
    .execute()
    .data
)

# Tri alphabétique NOM → PRÉNOM
membres = sorted(membres, key=lambda m: (m["nom"].lower(), m["prenom"].lower()))

# ---------------------------------------------------------
# Recherche
# ---------------------------------------------------------
search = st.text_input("🔍 Rechercher un membre")

if search:
    search_lower = search.lower()
    membres = [
        m for m in membres
        if search_lower in m["nom"].lower()
        or search_lower in m["prenom"].lower()
        or search_lower in str(m.get("email", "")).lower()
    ]

# ---------------------------------------------------------
# Affichage moderne
# ---------------------------------------------------------

def ligne_style(index):
    return (
        "background-color: #f7f7f7; padding: 8px; border-radius: 4px;"
        if index % 2 == 0
        else "padding: 8px;"
    )

# Colonnes élargies
header = st.columns([3, 3, 3, 4, 1])
header[0].markdown("**Nom**")
header[1].markdown("**Prénom**")
header[2].markdown("**Téléphone**")
header[3].markdown("**Email**")
header[4].markdown("**Fiche**")

st.markdown("---")

for index, membre in enumerate(membres):

    prenom = membre.get("prenom", "")
    nom = membre.get("nom", "")
    telephone = membre.get("telephone", "")
    email = membre.get("email", "")

    cols = st.columns([3, 3, 3, 4, 1])

    cols[0].markdown(f"<div style='{ligne_style(index)}'>{nom}</div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div style='{ligne_style(index)}'>{prenom}</div>", unsafe_allow_html=True)
    cols[2].markdown(f"<div style='{ligne_style(index)}'>📞 {telephone}</div>", unsafe_allow_html=True)
    cols[3].markdown(f"<div style='{ligne_style(index)}'>📧 {email}</div>", unsafe_allow_html=True)

    if cols[4].button("🔍", key=f"fiche_membre_{membre['id']}"):
        st.session_state["membre_id"] = membre["id"]
        st.switch_page("pages/21_Fiche_Membre.py")

st.markdown("---")

# Bouton ajouter membre — version correcte
if st.button("➕ Ajouter un membre"):
    st.session_state["membre_id"] = None
    st.switch_page("pages/01_Ajout_Membre.py")

