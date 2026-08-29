import streamlit as st
from supabase import create_client, Client
from menu import hide_streamlit_menu, menu_lateral

hide_streamlit_menu()
menu_lateral()

# --- Connexion Supabase ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("🔁 Transformation d'un extérieur en membre")

# ---------------------------------------------------------
# Charger uniquement les extérieurs validés (présence NON obligatoire)
# ---------------------------------------------------------
preins = (
    supabase.table("preinscriptions")
    .select("*")
    .eq("type", "exterieur")
    .eq("traitee", True)
    .eq("acceptee", True)
    .execute()
    .data
)

if not preins:
    st.info("Aucun extérieur à transformer.")
    st.stop()

# ---------------------------------------------------------
# Sélection
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 1️⃣ TRANSFORMER EN MEMBRE
# ---------------------------------------------------------
if st.button("Transformer en membre"):

    # Créer le membre
    membre_insert = supabase.table("membres").insert({
        "nom": choix["nom"],
        "prenom": choix["prenom"],
        "email": choix["email"],
        "telephone": choix["telephone"],
        "statut": "membre",
        "actif": False
    }).execute()

    membre_id = membre_insert.data[0]["id"]

    # Créer le chien
    chien_insert = supabase.table("chiens").insert({
        "nom": choix["chien_nom"],
        "race": choix["chien_race"],
        "id_membre": membre_id
    }).execute()

    chien_id = chien_insert.data[0]["id"]

    # Mise à jour de la préinscription
    supabase.table("preinscriptions").update({
        "membre_id": membre_id,
        "chien_id": chien_id,
        "type": "membre",
        "statut": "transforme"
    }).eq("id", choix["id"]).execute()

    st.success("✅ L'extérieur a été transformé en membre.")
    st.rerun()

# ---------------------------------------------------------
# 2️⃣ CLÔTURER LA PRÉINSCRIPTION (ARRÊT)
# ---------------------------------------------------------
if st.button("Clôturer la préinscription (arrêt)"):

    supabase.table("preinscriptions").update({
        "type": "cloturee",
        "statut": "archive"
    }).eq("id", choix["id"]).execute()

    st.warning("🗂️ La préinscription a été clôturée.")
    st.rerun()
