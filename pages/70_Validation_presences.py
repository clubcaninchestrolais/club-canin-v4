import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# Sécurité
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

# Connexion Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Validation des présences du jour")

# Séance du jour
aujourdhui = datetime.now().date().isoformat()

seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("date_seance", aujourdhui)
    .execute()
    .data
)

if not seances:
    st.info("Aucune séance aujourd'hui.")
    st.stop()

seance = seances[0]
seance_id = seance["id"]

st.subheader(f"Séance du {seance['date_seance']} — {seance.get('nom_seance', 'Séance')}")

# EXTÉRIEURS : on lit directement les préinscriptions acceptées
ext_preinscriptions = (
    supabase.table("preinscriptions")
    .select("*")
    .eq("seance_id", seance_id)
    .eq("acceptee", True)
    .execute()
    .data
)

if not ext_preinscriptions:
    st.info("Aucune présence extérieure à valider.")
else:
    st.markdown("### Présences extérieures")
    for pre in ext_preinscriptions:
        st.markdown("---")
        st.write(f"👤 {pre['prenom']} {pre['nom']} — 🐶 {pre['chien_nom']}")

        if not pre.get("presence_validee", False):
            if st.button(f"Valider présence extérieur #{pre['id']}", key=f"ext_{pre['id']}"):
                supabase.table("preinscriptions").update({
                    "presence_validee": True
                }).eq("id", pre["id"]).execute()
                st.success("Présence extérieure validée.")
                st.rerun()
        else:
            st.success("Présence déjà validée (extérieur).")
