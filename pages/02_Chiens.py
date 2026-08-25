import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

import datetime
from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Chiens", page_icon="🐶", layout="wide")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("Liste des chiens actifs")

# Charger uniquement les chiens NON archivés
chiens = (
    supabase.table("chiens")
    .select("*")
    .eq("archive", False)
    .execute()
    .data
)

# --- Tri sécurisé ---
chiens = sorted(
    chiens,
    key=lambda c: (
        str(c.get("nom", "") or "").lower(),
        str(c.get("race", "") or "").lower()
    )
)

def format_date(date_str):
    if not date_str:
        return "N/A"
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    except:
        return date_str

def calcul_age(date_str):
    if not date_str:
        return "N/A"
    try:
        dn = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        age = today.year - dn.year - ((today.month, today.day) < (dn.month, dn.day))
        return f"{age} ans"
    except:
        return "N/A"

# --- Recherche sécurisée ---
search = st.text_input("🔍 Rechercher un chien")

if search:
    search_lower = search.lower()
    chiens = [
        c for c in chiens
        if search_lower in str(c.get("nom", "") or "").lower()
        or search_lower in str(c.get("race", "") or "").lower()
        or search_lower in str(c.get("identification", "") or "").lower()
    ]

def ligne_style(index):
    return (
        "background-color: #f7f7f7; padding: 8px; border-radius: 4px;"
        if index % 2 == 0
        else "padding: 8px;"
    )

header = st.columns([3, 2, 4, 4, 1])
header[0].markdown("**Nom**")
header[1].markdown("**Race**")
header[2].markdown("**Naissance / Âge**")
header[3].markdown("**Propriétaire**")
header[4].markdown("**Fiche**")

st.markdown("---")

for index, chien in enumerate(chiens):

    nom = chien.get("nom", "")
    race = chien.get("race", "")
    naissance = chien.get("date_naissance", "")
    age = calcul_age(naissance)

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

    cols = st.columns([3, 2, 4, 4, 1])

    cols[0].markdown(f"<div style='{ligne_style(index)}'>{nom}</div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div style='{ligne_style(index)}'>{race}</div>", unsafe_allow_html=True)
    cols[2].markdown(
        f"<div style='{ligne_style(index)}'>📅 {format_date(naissance)} — 🎂 {age}</div>",
        unsafe_allow_html=True
    )
    cols[3].markdown(f"<div style='{ligne_style(index)}'>👤 {membre_nom}</div>", unsafe_allow_html=True)

    if cols[4].button("🔍", key=f"fiche_chien_{chien['id']}"):
        st.session_state["chien_id"] = chien["id"]
        st.switch_page("pages/_fiche_chien_page.py")

st.markdown("---")

if st.button("➕ Ajouter un chien"):
    st.session_state["membre_id"] = None
    st.switch_page("pages/22_Ajout_Chien.py")

