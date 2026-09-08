import streamlit as st
from securite import securite_admin
securite_admin()

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral
from datetime import datetime

hide_streamlit_menu()
menu_lateral()

st.title("ℹ️ Version du programme")

# Charger les versions (tri fiable)
versions = (
    supabase.table("versions")
    .select("*")
    .order("created_at", desc=True)
    .execute()
    .data
)

# ---------------------------------------------------------
# Si aucune version
# ---------------------------------------------------------
if not versions:
    st.info("Aucune version enregistrée.")
else:
    # Version actuelle = première entrée après tri
    version_actuelle = versions[0]

    st.subheader("Version actuelle")

    st.write(f"### 🟢 Version {version_actuelle['version']}")
    st.write(f"**Dernière mise à jour :** {version_actuelle['last_update']}")
    st.write(f"**Build :** {version_actuelle['build']}")
    st.write(f"**Enregistrée le :** {version_actuelle['created_at']}")

st.markdown("---")

# ---------------------------------------------------------
# Ajouter une nouvelle version
# ---------------------------------------------------------
st.subheader("➕ Ajouter une nouvelle version")

with st.form("form_version"):
    new_version = st.text_input("Numéro de version (ex : 4.1)")
    new_last_update = st.date_input("Date de mise à jour", datetime.now())
    new_build = st.text_area("Notes de build / description")

    submit = st.form_submit_button("💾 Enregistrer la nouvelle version")

if submit:
    supabase.table("versions").insert({
        "version": new_version,
        "last_update": new_last_update.isoformat(),
        "build": new_build,
    }).execute()

    st.success("Nouvelle version enregistrée.")
    st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Historique complet
# ---------------------------------------------------------
st.subheader("Historique des versions")

if versions:
    for v in versions:
        with st.expander(f"📌 Version {v['version']} — {v['last_update']}"):
            st.write(f"**Build :** {v['build']}")
            st.write(f"**Créée le :** {v['created_at']}")
            st.write(f"**ID interne :** {v['id']}")
