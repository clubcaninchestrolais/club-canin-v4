import streamlit as st
from supabase_rest import supabase

st.set_page_config(page_title="Cours", page_icon="📚")

st.title("📚 Types de cours")

# ---------------------------------------------------------
# Bouton : Ajouter un cours
# ---------------------------------------------------------
if st.button("➕ Ajouter un cours"):
    st.switch_page("pages/05_Ajouter_Cours.py")

st.markdown("---")

# ---------------------------------------------------------
# Charger la liste des cours
# ---------------------------------------------------------
response = supabase.table("cours").select("*").order("nom").execute()
cours_list = response.data

if not cours_list:
    st.info("Aucun cours pour le moment. Ajoutez un cours pour commencer.")
    st.stop()

# ---------------------------------------------------------
# Affichage de la liste des cours
# ---------------------------------------------------------
for cours in cours_list:
    with st.container():
        st.subheader(cours["nom"])
        st.write(cours["description"] or "Aucune description")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(f"✏️ Modifier", key=f"edit_{cours['id']}"):
                st.session_state["cours_id"] = cours["id"]
                st.switch_page("pages/05_Modifier_Cours.py")

        with col2:
            if st.button(f"🗑️ Supprimer", key=f"delete_{cours['id']}"):
                supabase.table("cours").delete().eq("id", cours["id"]).execute()
                st.rerun()

        with col3:
            if st.button(f"📅 Séances", key=f"seances_{cours['id']}"):
                st.session_state["cours_id"] = cours["id"]
                st.switch_page("pages/07_Seances_Cours.py")

        st.markdown("---")
