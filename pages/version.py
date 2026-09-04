import streamlit as st
from securite import securite_admin
securite_admin()

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

hide_streamlit_menu()
menu_lateral()

st.title("ℹ️ Version du programme")

# Charger les versions
versions = (
    supabase.table("versions")   # ✔️ nom correct de la table
    .select("*")
    .order("last_update", desc=True)   # ✔️ colonne existante
    .execute()
    .data
)

if not versions:
    st.info("Aucune version enregistrée.")
    st.stop()

# Version actuelle
version_actuelle = versions[0]

st.subheader("Version actuelle")

st.write(f"### 🟢 Version {version_actuelle['version']}")
st.write(f"**Dernière mise à jour :** {version_actuelle
