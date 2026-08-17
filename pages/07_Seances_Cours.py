import streamlit as st
from supabase_rest import supabase

st.set_page_config(page_title="Séances du cours", page_icon="📅")
st.title("📅 Séances du cours")

# Vérifier que le cours est bien sélectionné
cours_id = st.session_state.get("cours_id")

if not cours_id:
    st.error("Aucun cours sélectionné.")
    st.stop()

# Charger le cours
cours = (
    supabase.table("cours")
    .select("*")
    .eq("id", cours_id)
    .execute()
    .data[0]
)

st.subheader(f"Cours : {cours['nom']}")
st.markdown("---")

# Boutons en haut
colA, colB = st.columns(2)

with colA:
    if st.button("➕ Ajouter une séance"):
        st.switch_page("pages/06_Ajouter_Seance.py")

with colB:
    if st.button("⬅️ Retour aux cours"):
        st.switch_page("pages/04_Cours.py")

# Charger les séances
seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("cours_id", cours_id)
    .eq("actif", True)
    .order("date_seance")
    .execute()
    .data
)

if not seances:
    st.info("Aucune séance active pour ce cours.")
    st.stop()

# Affichage des séances
for seance in seances:
    with st.container():
        st.write(
            f"📅 **{seance['date_seance']}** — "
            f"{seance['heure_debut']} → {seance['heure_fin']}"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button(f"✏️ Modifier", key=f"edit_{seance['id']}"):
                st.session_state["seance_id"] = seance["id"]
                st.switch_page("pages/08_Modifier_Seance.py")

        with col2:
            if st.button(f"📝 Inscriptions", key=f"inscr_{seance['id']}"):
                st.session_state["seance_id"] = seance["id"]
                st.switch_page("pages/09_Inscription_Seance.py")

        with col3:
            if st.button(f"📦 Archiver", key=f"archive_{seance['id']}"):
                supabase.table("cours_seances").update({"actif": False}).eq("id", seance["id"]).execute()
                st.rerun()

        with col4:
            if st.button(f"🗑️ Supprimer", key=f"delete_{seance['id']}"):
                supabase.table("cours_seances").delete().eq("id", seance["id"]).execute()
                st.rerun()

        st.markdown("---")
