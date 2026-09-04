import streamlit as st
from securite import securite_admin
securite_admin()

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

hide_streamlit_menu()
menu_lateral()

st.title("ℹ️ Version du programme")

# Charger les versions (tri fiable)
versions = (
    supabase.table("versions")
    .select("*")
    .order("created_at", desc=True)   # ✔️ la dernière version en premier
    .execute()
    .data
)

if not versions:
    st.info("Aucune version enregistrée.")
    st.stop()

# Version actuelle = première entrée après tri
version_actuelle = versions[0]

st.subheader("Version actuelle")

st.write(f"### 🟢 Version {version_actuelle['version']}")
st.write(f"**Dernière mise à jour :** {version_actuelle['last_update']}")
st.write(f"**Build :** {version_actuelle['build']}")
st.write(f"**Enregistrée le :** {version_actuelle['created_at']}")

st.markdown("---")

# Historique complet
st.subheader("Historique des versions")

for v in versions:
    with st.expander(f"📌 Version {v['version']} — {v['last_update']}"):
        st.write(f"**Build :** {v['build']}")
        st.write(f"**Créée le :** {v['created_at']}")
        st.write(f"**ID interne :** {v['id']}")
