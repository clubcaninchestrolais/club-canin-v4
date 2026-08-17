import streamlit as st
from supabase_rest import supabase

st.set_page_config(page_title="Accueil — Cours", page_icon="📘")
st.title("📘 Accueil des cours")

# ---------------------------------------------------------
# Charger les cours
# ---------------------------------------------------------
cours = (
    supabase.table("cours")
    .select("*")
    .order("id")
    .execute()
    .data
)

if not cours:
    st.error("Aucun cours trouvé.")
    st.stop()

st.subheader("Liste des cours")

for c in cours:
    st.markdown("---")
    st.write(f"### 🐾 Cours {c['id']} — {c['nom']}")

    st.write(f"📄 Description : {c.get('description', 'Aucune description')}")

    # Charger les séances du cours
    seances = (
        supabase.table("cours_seances")
        .select("*")
        .eq("cours_id", c["id"])
        .order("date_seance")
        .execute()
        .data
    )

    if not seances:
        st.info("Aucune séance programmée pour ce cours.")
        continue

    st.write("#### 📅 Séances programmées :")

    for s in seances:
        st.write(
            f"- **{s['date_seance']}** à **{s['heure_debut']}** "
            f"(ID séance : {s['id']})"
        )

        col1, col2 = st.columns(2)

        # Bouton inscription
        if col1.button(
            f"Inscrire un membre — séance {s['id']}",
            key=f"inscrire_{s['id']}"
        ):
            st.query_params["cours_id"] = c["id"]
            st.query_params["seance_id"] = s["id"]
            st.switch_page("32_Seance_inscription.py")

        # Bouton validation des présences
        if col2.button(
            f"Valider présences — séance {s['id']}",
            key=f"valider_{s['id']}"
        ):
            st.query_params["cours_id"] = c["id"]
            st.query_params["seance_id"] = s["id"]
            st.switch_page("70_Validation_Presences.py")
