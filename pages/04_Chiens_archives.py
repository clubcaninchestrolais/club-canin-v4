import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("01_Connexion.py")

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

st.set_page_config(page_title="Chiens archivés", page_icon="🗃️")

hide_streamlit_menu()
menu_lateral()

st.title("Chiens archivés")

chiens = (
    supabase.table("chiens")
    .select("*")
    .eq("archive", True)
    .execute()
    .data
)

st.write("### Chiens archivés")

def ligne_style(index):
    return (
        "background-color: #f7f7f7; padding: 6px; border-radius: 4px;"
        if index % 2 == 0
        else "padding: 6px;"
    )

header = st.columns([2, 2, 2, 2, 1])
header[0].markdown("**Nom**")
header[1].markdown("**Race**")
header[2].markdown("**Naissance**")
header[3].markdown("**Membre**")
header[4].markdown("**Fiche**")

st.markdown("---")

for index, chien in enumerate(chiens):

    nom = chien.get("nom", "")
    race = chien.get("race", "")
    naissance = chien.get("date_naissance", "")
    id_membre = chien.get("id_membre", None)

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

    if cols[4].button("🔍", key=f"fiche_chien_arch_{chien['id']}"):
        st.session_state["chien_id"] = chien["id"]
        st.switch_page("06_fiche_chien.py")   # <-- CORRECTION FINALE

st.markdown("---")
