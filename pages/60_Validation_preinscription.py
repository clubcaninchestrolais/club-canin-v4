import streamlit as st
from supabase import create_client, Client

# Sécurité
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

# Connexion Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Validation des préinscriptions (extérieurs)")

# Charger les préinscriptions non traitées
preinscriptions = (
    supabase.table("preinscriptions")
    .select("*")
    .eq("traitee", False)
    .execute()
    .data
)

if not preinscriptions:
    st.info("Aucune préinscription à valider.")
    st.stop()

for pre in preinscriptions:
    st.markdown("---")
    st.write(f"👤 {pre['prenom']} {pre['nom']}")
    st.write(f"🐶 {pre['chien_nom']}")
    st.write(f"📅 Séance ID : {pre['seance_id']}")

    if st.button(f"Valider préinscription #{pre['id']}", key=f"valider_{pre['id']}"):

        # On ne touche plus à cours_seances_inscriptions
        supabase.table("preinscriptions").update({
            "traitee": True,
            "acceptee": True
        }).eq("id", pre["id"]).execute()

        st.success("Préinscription validée (extérieur).")
        st.rerun()
