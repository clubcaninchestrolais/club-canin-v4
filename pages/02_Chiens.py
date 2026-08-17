import streamlit as st
from supabase_rest import supabase

#version 160825H1132
st.set_page_config(page_title="Chiens", page_icon="🐶")

st.title("Liste des chiens actifs")

# Charger uniquement les chiens NON archivés
chiens = (
    supabase.table("chiens")
    .select("*")
    .eq("archive", False)
    .execute()
    .data
)

# ---------------------------------------------------------
# Recherche
# ---------------------------------------------------------
search = st.text_input("🔍 Rechercher un chien")

if search:
    search_lower = search.lower()
    chiens = [
        c for c in chiens
        if search_lower in c.get("nom", "").lower()
        or search_lower in c.get("race", "").lower()
        or search_lower in str(c.get("identification", "")).lower()
    ]

# ---------------------------------------------------------
# Affichage moderne
# ---------------------------------------------------------

def ligne_style(index):
    return (
        "background-color: #f7f7f7; padding: 6px; border-radius: 4px;"
        if index % 2 == 0
        else "padding: 6px;"
    )

header = st.columns([2, 2, 2, 2, 1])
header[0].markdown("**Nom**")
header[1].markdown("**Raceduchien**")   # ← C’EST CETTE LIGNE QUI AFFECTE LE TITRE
header[2].markdown("**Naissance**")
header[3].markdown("**Propriétaire**")
header[4].markdown("**Fiche**")

st.markdown("---")

for index, chien in enumerate(chiens):

    nom = chien.get("nom", "")
    race = chien.get("race", "")   # ← C’EST CETTE LIGNE QUI AFFECTE LA VALEUR
    naissance = chien.get("date_naissance", "")
    id_membre = chien.get("id_membre", None)

    # Charger le propriétaire
    membre_nom = "Inconnu"
    if id_membre:
        membre = (
            supabase.table("membres")
            .select("prenom, nom")
            .eq("id", id_membre)
            .execute()
            .data
        )
        if membre:
            membre_nom = f"{membre[0]['prenom']} {membre[0]['nom']}"

    cols = st.columns([2, 2, 2, 2, 1])

    cols[0].markdown(f"<div style='{ligne_style(index)}'>{nom}</div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div style='{ligne_style(index)}'>{race}</div>", unsafe_allow_html=True)
    cols[2].markdown(f"<div style='{ligne_style(index)}'>📅 {naissance}</div>", unsafe_allow_html=True)
    cols[3].markdown(f"<div style='{ligne_style(index)}'>👤 {membre_nom}</div>", unsafe_allow_html=True)

    # Bouton fiche chien
    if cols[4].button("🔍", key=f"fiche_chien_{chien['id']}"):
        st.session_state["chien_id"] = chien["id"]
        st.switch_page("pages/_fiche_chien_page.py")

st.markdown("---")

# ---------------------------------------------------------
# Bouton ajouter
# ---------------------------------------------------------
if st.button("➕ Ajouter un chien"):
    st.session_state["membre_id"] = None
    st.switch_page("pages/22_Ajout_Chien.py")
