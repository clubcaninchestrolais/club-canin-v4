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

# ---------------------------------------------------------
# 1️⃣ BOUTON : TRANSFORMER EN MEMBRE
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

    if not membre_insert.data:
        st.error("❌ Supabase a refusé l'insertion du membre.")
        st.json(membre_insert)
        st.stop()

    membre_id = membre_insert.data[0]["id"]

    # Créer le chien
    chien_insert = supabase.table("chiens").insert({
        "nom": choix["chien_nom"],
        "race": choix["chien_race"],
        "id_membre": membre_id
    }).execute()

    if not chien_insert.data:
        st.error("❌ Supabase a refusé l'insertion du chien.")
        st.json(chien_insert)
        st.stop()

    chien_id = chien_insert.data[0]["id"]

    # Mise à jour de la préinscription
    supabase.table("preinscriptions").update({
        "archive": True,
        "actif": False,
        "present_exterieur": choix["present_exterieur"] or False,
        "membre_id": membre_id,
        "chien_id": chien_id,
        "type": "membre"
    }).eq("id", choix["id"]).execute()

    st.success("✅ L'extérieur a été transformé en membre.")
    st.info("Vous pouvez maintenant compléter les informations du membre via le menu 'Membres'.")
    st.rerun()

# ---------------------------------------------------------
# 2️⃣ BOUTON : CLÔTURER LA PRÉINSCRIPTION (ARRÊT)
# ---------------------------------------------------------
if st.button("Clôturer la préinscription (arrêt)"):

    supabase.table("preinscriptions").update({
        "archive": True,
        "actif": False,
        "present_exterieur": choix["present_exterieur"] or False
    }).eq("id", choix["id"]).execute()

    st.warning("🗂️ La préinscription a été clôturée.")
    st.rerun()
