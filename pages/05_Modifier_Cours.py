import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase

st.set_page_config(page_title="Modifier un cours", page_icon="✏️")

st.title("✏️ Modifier un type de cours")

cours_id = st.session_state.get("cours_id")

if not cours_id:
    st.error("Aucun cours sélectionné.")
    st.stop()

response = supabase.table("cours").select("*").eq("id", cours_id).execute()
cours = response.data[0]

nom = st.text_input("Nom du cours", cours["nom"])
description = st.text_area("Description", cours["description"])
actif = st.checkbox("Actif", value=cours["actif"])

st.markdown("---")

if st.button("💾 Enregistrer"):
    data = {
        "nom": nom,
        "description": description,
        "actif": actif
    }
    supabase.table("cours").update(data).eq("id", cours_id).execute()
    st.success("Cours mis à jour.")
    st.switch_page("pages/04_Cours.py")

if st.button("🗑️ Supprimer"):
    supabase.table("cours").delete().eq("id", cours_id).execute()
    st.success("Cours supprimé.")
    st.switch_page("pages/04_Cours.py")

if st.button("⬅️ Retour"):
    st.switch_page("pages/04_Cours.py")
