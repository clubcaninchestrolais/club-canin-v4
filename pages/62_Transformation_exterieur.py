import streamlit as st
from supabase import create_client, Client
from menu import hide_streamlit_menu, menu_lateral
import datetime

hide_streamlit_menu()
menu_lateral()

# --- Connexion Supabase ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("🔁 Transformation d'un extérieur en membre")

# --- Charger les préinscriptions extérieures ---
preins = (
    supabase.table("preinscriptions")
    .select("*")
    .eq("type", "exterieur")
    .order("date_seance")
    .execute()
    .data
)

if not preins:
    st.info("Aucun extérieur à transformer.")
    st.stop()

# --- Sélection ---
choix = st.selectbox(
    "Sélectionner un extérieur",
    options=preins,
    format_func=lambda p: f"{p['prenom']} {p['nom']} — {p['email']}"
)

st.subheader("Informations de l'extérieur")
st.write(f"**Nom :** {choix['nom']}")
st.write(f"**Prénom :** {choix['prenom']}")
st.write(f"**Email :** {choix['email']}")
st.write(f"**Téléphone :** {choix['telephone']}")
st.write(f"**Chien :** {choix['chien_nom']} ({choix['chien_race']})")

st.markdown("---")

# --- Transformation ---
if st.button("Transformer en membre"):

    # 1️⃣ Créer le membre (minimal)
    membre_insert = supabase.table("membres").insert({
        "nom": choix["nom"],
        "prenom": choix["prenom"],
        "email": choix["email"],
        "telephone": choix["telephone"],
        "statut": "membre",
        "actif": False
    }).execute()

    # Vérification d'erreur Supabase
    if not membre_insert.data:
        st.error("❌ Supabase a refusé l'insertion du membre. Un champ obligatoire manque dans la table 'membres'.")
        st.stop()

    membre_id = membre_insert.data[0]["id"]

    # 2️⃣ Créer le chien (minimal)
    chien_insert = supabase.table("chiens").insert({
        "nom": choix["chien_nom"],
        "race": choix["chien_race"],
        "id_membres": membre_id
    }).execute()

    if not chien_insert.data:
        st.error("❌ Supabase a refusé l'insertion du chien.")
        st.stop()

    chien_id = chien_insert.data[0]["id"]

    # 3️⃣ Mettre à jour la préinscription
    supabase.table("preinscriptions").update({
        "type": "membre",
        "membre_id": membre_id,
        "chien_id": chien_id
    }).eq("id", choix["id"]).execute()

    st.success("✅ L'extérieur a été transformé en membre.")
    st.info("Vous pouvez maintenant compléter les informations du membre via le menu 'Membres'.")
    st.experimental_rerun()
