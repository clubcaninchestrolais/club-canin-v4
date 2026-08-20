import streamlit as st
from supabase_rest import supabase

st.set_page_config(page_title="Validation préposé", page_icon="🧩")
st.title("🧩 Validation des préinscriptions")

# Charger les préinscriptions
preinscriptions = (
    supabase.table("preinscriptions")
    .select("*")
    .order("id", desc=False)
    .execute()
    .data
)

if not preinscriptions:
    st.info("Aucune préinscription en attente.")
    st.stop()

for p in preinscriptions:
    st.markdown("---")
    st.write(f"### {p['prenom']} {p['nom']} — {p['type']}")

    st.write(f"- Cours : {p['cours_id']}")
    st.write(f"- Séance : {p['seance_id']}")
    st.write(f"- Membre ID : {p['membre_id']}")
    st.write(f"- Chien ID : {p['chien_id']}")

    if st.button(f"Valider préinscription #{p['id']}", key=f"val_{p['id']}"):

        # 1️⃣ CAS MEMBRE → inscription automatique
        if p["type"] == "membre":
            supabase.table("cours_seances_inscriptions").insert({
                "seance_id": p["seance_id"],
                "membre_id": p["membre_id"],
                "chien_id": p["chien_id"],
                "present": False
            }).execute()

            st.success(f"Membre validé — inscrit automatiquement.")

        # 2️⃣ CAS EXTERIEUR → création présence automatique
        elif p["type"] == "exterieur":

            # Récupérer la date de la séance
            seance = (
                supabase.table("cours_seances")
                .select("date_seance")
                .eq("id", p["seance_id"])
                .execute()
                .data[0]
            )
            date_seance = seance["date_seance"]

            # Insérer la présence
            supabase.table("cours_presences").insert({
                "seance_id": p["seance_id"],
                "membre_id": p["membre_id"],
                "chien_id": p["chien_id"],
                "date_presence": date_seance,
                "present": False
            }).execute()

            st.success(f"Extérieur validé — présence créée.")

        else:
            st.error("Préinscription invalide.")
            st.stop()

        # Supprimer la préinscription
        supabase.table("preinscriptions").delete().eq("id", p["id"]).execute()

        st.info("Préinscription supprimée.")
        st.rerun()
