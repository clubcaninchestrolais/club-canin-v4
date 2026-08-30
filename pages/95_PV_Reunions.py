import streamlit as st
from securite import securite_admin
securite_admin()

from datetime import date
from supabase_rest import supabase

st.title("📄 PV des réunions")

st.write("Cette page permet de créer, consulter et archiver les PV des réunions du comité.")

# ---------------------------------------------------------
# Création d'un PV
# ---------------------------------------------------------

st.subheader("Créer un nouveau PV")

titre = st.text_input("Titre du PV")
date_reunion = st.date_input("Date de la réunion", value=date.today())
contenu = st.text_area("Contenu du PV (compte rendu complet)")

if st.button("Enregistrer le PV"):
    data = {
        "titre": titre,
        "contenu": contenu,
        "date_reunion": str(date_reunion),
        "auteur": st.session_state.get("user_id", "admin")
    }
    supabase.table("pv_reunions").insert(data).execute()
    st.success("PV enregistré avec succès !")

st.markdown("---")

# ---------------------------------------------------------
# Liste des PV existants
# ---------------------------------------------------------

st.subheader("PV enregistrés")

pvs = (
    supabase.table("pv_reunions")
    .select("*")
    .order("date_reunion", desc=True)
    .execute()
    .data
)

if not pvs:
    st.info("Aucun PV enregistré pour le moment.")
else:
    for pv in pvs:
        with st.expander(f"📅 {pv['date_reunion']} — {pv['titre']}"):
            st.write(f"**Auteur :** {pv['auteur']}")
            st.write(f"**Créé le :** {pv['date_creation']}")
            st.markdown("---")
            st.write(pv["contenu"])

            # Bouton supprimer
            if st.button("🗑️ Supprimer ce PV", key=f"delete_{pv['id']}"):
                supabase.table("pv_reunions").delete().eq("id", pv["id"]).execute()
                st.rerun()
