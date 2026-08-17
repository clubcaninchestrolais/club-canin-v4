import streamlit as st
from supabase_rest import supabase

def afficher_page_membres():
    st.title("Gestion des membres")

    membres = supabase.table("membres").select("*").order("id").execute().data

    search = st.text_input("🔍 Rechercher un membre")

    if search.strip():
        s = search.lower()
        membres = [
            m for m in membres
            if s in m["prenom"].lower()
            or s in m["nom"].lower()
            or s in (m["email"] or "").lower()
        ]

    st.dataframe(membres)

    if membres:
        choix = st.selectbox(
            "Sélectionnez un membre",
            membres,
            format_func=lambda m: f"{m['prenom']} {m['nom']} (ID {m['id']})"
        )

        if st.button("📄 Voir la fiche du membre"):
            st.session_state["membre_id"] = choix["id"]
            st.session_state["page"] = "fiche_membre"
            st.rerun()
