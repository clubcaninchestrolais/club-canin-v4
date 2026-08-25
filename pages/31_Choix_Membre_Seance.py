import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase import create_client

st.set_page_config(page_title="Choix du membre", page_icon="🐾")

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("🐾 Inscription à une séance — Choix du membre")

# ---------------------------------------------------------
# Charger les membres actifs
# ---------------------------------------------------------
membres = (
    supabase.table("membres")
    .select("*")
    .eq("archive", False)
    .order("nom")
    .execute()
    .data
)

if not membres:
    st.error("Aucun membre trouvé.")
    st.stop()

# ---------------------------------------------------------
# Filtre de recherche
# ---------------------------------------------------------
filtre = st.text_input("🔍 Rechercher un membre (nom ou prénom)")

if filtre:
    filtre_lower = filtre.lower()
    membres = [
        m for m in membres
        if filtre_lower in m["nom"].lower()
        or filtre_lower in m["prenom"].lower()
    ]

# ---------------------------------------------------------
# Affichage compact des membres
# ---------------------------------------------------------
st.subheader("👤 Sélection du membre")

for m in membres:
    col1, col2 = st.columns([4, 1])

    with col1:
        st.write(f"**{m['nom']} {m['prenom']}**")

    with col2:
        if st.button("Inscrire", key=f"inscrire_{m['id']}"):
            st.session_state["membre_id"] = m["id"]
            st.switch_page("pages/32_Seance_inscription.py")
