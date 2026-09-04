import streamlit as st
from securite import securite_admin
securite_admin()

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

hide_streamlit_menu()
menu_lateral()

st.title("👨‍🏫 Gestion des moniteurs")

# ---------------------------------------------------------
# Charger les moniteurs
# ---------------------------------------------------------

moniteurs = (
    supabase.table("moniteurs")
    .select("*")
    .order("nom")
    .execute()
    .data
)

st.subheader("Liste des moniteurs")

if not moniteurs:
    st.info("Aucun moniteur enregistré pour le moment.")
else:
    for m in moniteurs:
        with st.expander(f"{m['nom']} — {m['email']}"):
            st.write(f"📞 Téléphone : {m['telephone']}")
            st.write(f"📧 Email : {m['email']}")

            # Suppression
            if st.button("🗑️ Supprimer", key=f"delete_{m['id']}"):
                supabase.table("moniteurs").delete().eq("id", m["id"]).execute()
                st.success("Moniteur supprimé.")
                st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Ajouter un moniteur
# ---------------------------------------------------------

st.subheader("Ajouter un moniteur")

nom = st.text_input("Nom")
telephone = st.text_input("Téléphone")
email = st.text_input("Email")

if st.button("Ajouter le moniteur"):
    if not nom or not email:
        st.error("Le nom et l'email sont obligatoires.")
    else:
        supabase.table("moniteurs").insert({
            "nom": nom,
            "telephone": telephone,
            "email": email
        }).execute()

        st.success("Moniteur ajouté avec succès.")
        st.rerun()
