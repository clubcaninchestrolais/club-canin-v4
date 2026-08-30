import streamlit as st
from securite import securite_admin
securite_admin()

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral


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

    col1, col2 = st.columns(2)

    # -----------------------------
    # BOUTON VALIDER
    # -----------------------------
    with col1:
        if st.button(f"Valider #{pre['id']}", key=f"valider_{pre['id']}"):
            supabase.table("preinscriptions").update({
                "traitee": True,
                "acceptee": True,
                "statut": "valide"
            }).eq("id", pre["id"]).execute()

            st.success("Préinscription validée.")
            st.rerun()

    # -----------------------------
    # BOUTON REJETER / ARCHIVER
    # -----------------------------
    with col2:
        if st.button(f"Rejeter #{pre['id']}", key=f"rejeter_{pre['id']}"):
            supabase.table("preinscriptions").update({
                "traitee": True,
                "acceptee": False,
                "statut": "archive"
            }).eq("id", pre["id"]).execute()

            st.warning("Préinscription rejetée et archivée.")
            st.rerun()
