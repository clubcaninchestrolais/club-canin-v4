import streamlit as st
from supabase import create_client, Client

# Sécurité
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

# Connexion Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Validation des préinscriptions")

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

        # Marquer la préinscription comme traitée et acceptée
        supabase.table("preinscriptions").update({
            "traitee": True,
            "acceptee": True
        }).eq("id", pre["id"]).execute()

        # INSÉRER DIRECTEMENT LES DONNÉES EXTÉRIEURES DANS cours_seances_inscriptions
        supabase.table("cours_seances_inscriptions").insert({
            "seance_id": pre["seance_id"],
            "type_inscription": "exterieur",
            "present": False,
            "actif": True,
            "nom_exterieur": pre["nom"],
            "prenom_exterieur": pre["prenom"],
            "chien_exterieur": pre["chien_nom"]
        }).execute()

        st.success("Préinscription validée et ajoutée à la séance.")
        st.rerun()
