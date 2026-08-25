import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase

st.set_page_config(page_title="Ajouter un cours", page_icon="📘")

st.title("📘 Ajouter un type de cours")

if st.button("⬅️ Retour"):
    st.switch_page("pages/04_Cours.py")

st.markdown("---")

nom = st.text_input("Nom du cours")
description = st.text_area("Description")
actif = st.checkbox("Actif", value=True)

st.markdown("---")

if st.button("➕ Créer le cours"):
    if not nom:
        st.error("Le nom du cours est obligatoire.")
    else:
        data = {
            "nom": nom,
            "description": description,
            "actif": actif
        }

        supabase.table("cours").insert(data).execute()
        st.success("Cours créé avec succès.")
        st.switch_page("pages/04_Cours.py")
