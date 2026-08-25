import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase import create_client, Client
from menu import hide_streamlit_menu, menu_lateral   # <-- AJOUT

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Validation préinscriptions", page_icon="✅", layout="centered")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()   # <-- AJOUT

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()          # <-- AJOUT

st.title("Validation des préinscriptions extérieures")

# ---------------------------------------------------------
# Charger les préinscriptions extérieures NON traitées
# ---------------------------------------------------------
res = (
    supabase.table("preinscriptions")
    .select("*")
    .eq("type", "exterieur")
    .eq("traitee", False)
    .execute()
)

preinscriptions = res.data or []

if not preinscriptions:
    st.info("Aucune préinscription extérieure à valider.")
    st.stop()

# ---------------------------------------------------------
# Affichage et actions
# ---------------------------------------------------------
for pre in preinscriptions:
    st.markdown("---")
    st.subheader(f"#{pre['id']} – {pre['prenom']} {pre['nom']}")

    st.write(f"**Email :** {pre.get('email', '')}")
    st.write(f"**Téléphone :** {pre.get('telephone', '')}")
    st.write(f"**Chien :** {pre.get('chien_nom', '')} ({pre.get('chien_race', '')})")
    st.write(f"**Cours ID :** {pre.get('cours_id', '')}")
    st.write(f"**Date préinscription :** {pre.get('date_preinscription', '')}")
    st.write(f"**Statut actuel :** {pre.get('statut', 'En attente')}")

    col1, col2 = st.columns(2)

    # VALIDATION
    with col1:
        if st.button(f"✅ Valider #{pre['id']}", key=f"valider_{pre['id']}"):
            supabase.table("preinscriptions").update(
                {
                    "statut": "valide",
                    "traitee": True,
                    "acceptee": True,
                }
            ).eq("id", pre["id"]).execute()

            st.success(f"Préinscription #{pre['id']} validée.")
            st.rerun()

    # REFUS
    with col2:
        if st.button(f"❌ Refuser #{pre['id']}", key=f"refuser_{pre['id']}"):
            supabase.table("preinscriptions").update(
                {
                    "statut": "refuse",
                    "traitee": True,
                    "acceptee": False,
                }
            ).eq("id", pre["id"]).execute()

            st.warning(f"Préinscription #{pre['id']} refusée.")
            st.rerun()




