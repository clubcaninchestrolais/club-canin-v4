import streamlit as st
from securite import securite_admin
securite_admin()

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

hide_streamlit_menu()
menu_lateral()

st.title("ℹ️ À propos — Version du programme")

# Charger les versions
versions = (
    supabase.table("version")
    .select("*")
    .order("last_update", desc=True)
    .execute()
    .data
)

if not versions:
    st.info("Aucune version enregistrée.")
    st.stop()

# Version actuelle (la plus récente)
version_actuelle = versions[0]

st.subheader("Version actuelle")

st.write(f"### 🟢 Version {version_actuelle['version']}")
st.write(f"**Dernière mise à jour :** {version_actuelle['last_update']}")
st.write(f"**Build :** {version_actuelle['build']}")
st.write(f"**Enregistrée le :** {version_actuelle['created_at']}")

st.markdown("---")

# Historique des versions
st.subheader("Historique des versions")

for v in versions:
    with st.expander(f"📌 Version {v['version']} — {v['last_update']}"):
        st.write(f"**Build :** {v['build']}")
        st.write(f"**Créée le :** {v['created_at']}")
        st.write(f"**ID interne :** {v['id']}")

st.markdown("---")

st.subheader("À propos du logiciel")

st.write("""
Ce logiciel a été développé pour le Club Canin de Neufchâteau afin de gérer :

- les membres et les chiens  
- les préinscriptions  
- les cours et les séances  
- les présences  
- les cotisations et abonnements  
- les finances  
- les PV des réunions  
- la sécurité et le monitoring

Il est mis à jour régulièrement pour améliorer les fonctionnalités, la stabilité et la sécurité.
""")
