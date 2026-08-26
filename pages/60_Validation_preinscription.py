import streamlit as st

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase import create_client, Client
from menu import hide_streamlit_menu, menu_lateral

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Validation préinscriptions", page_icon="✅", layout="centered")

hide_streamlit_menu()
menu_lateral()

st.title("Validation des préinscriptions extérieures")

# ---------------------------------------------------------
# Charger les préinscriptions extérieures NON traitées
# ---------------------------------------------------------
res = (
    supabase.table("preinscriptions")
    .select("*")
    .eq("type", "exterieur")
    .eq("traitee", False)
    .eq("acceptee", False)
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
    st.write(f"**Séance ID :** {pre.get('seance_id', '')}")
    st.write(f"**Date préinscription :** {pre.get('date_preinscription', '')}")

    col1, col2 = st.columns(2)

    # VALIDATION
    with col1:
        if st.button(f"✅ Valider #{pre['id']}", key=f"valider_{pre['id']}"):

            try:
                # 1️⃣ Marquer la préinscription comme validée
                update_pre = supabase.table("preinscriptions").update(
                    {
                        "traitee": True,
                        "acceptee": True,
                    }
                ).eq("id", pre["id"]).execute()

                st.write("DEBUG update_pre:", update_pre)

                # 2️⃣ Créer un membre temporaire (corrigé)
                membre = supabase.table("membres").insert({
                    "nom": pre["nom"],
                    "prenom": pre["prenom"],
                    "email": pre["email"],
                    "telephone": pre["telephone"],
                    "actif": True
                }).execute()

                st.write("DEBUG membre:", membre)

                membre_id = membre.data[0]["id"]

                # 3️⃣ Créer un chien temporaire
                chien = supabase.table("chiens").insert({
                    "nom": pre["chien_nom"],
                    "race": pre["chien_race"],
                    "id_membre": membre_id
                }).execute()

                st.write("DEBUG chien:", chien)

                chien_id = chien.data[0]["id"]

                # 4️⃣ Créer l'inscription dans la séance
                inscription = supabase.table("cours_seances_inscriptions").insert({
                    "seance_id": pre["seance_id"],
                    "membre_id": membre_id,
                    "chien_id": chien_id,
                    "present": False,
                    "commentaire": None,
                    "actif": True
                }).execute()

                st.write("DEBUG inscription:", inscription)

                st.success(f"Préinscription #{pre['id']} validée et ajoutée à la séance.")
                st.rerun()

            except Exception as e:
                st.error("ERREUR SUPABASE :")
                st.write(e)

    # REFUS
    with col2:
        if st.button(f"❌ Refuser #{pre['id']}", key=f"refuser_{pre['id']}"):

            try:
                refuse = supabase.table("preinscriptions").update(
                    {
                        "traitee": True,
                        "acceptee": False,
                    }
                ).eq("id", pre["id"]).execute()

                st.write("DEBUG refuse:", refuse)

                st.warning(f"Préinscription #{pre['id']} refusée.")
                st.rerun()

            except Exception as e:
                st.error("ERREUR SUPABASE :")
                st.write(e)

