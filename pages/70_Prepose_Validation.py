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

    # Affichage des infos
    st.write(f"- Cours : {p['cours_id']}")
    st.write(f"- Séance : {p['seance_id']}")
    st.write(f"- Membre ID : {p['membre_id']}")
    st.write(f"- Chien ID : {p['chien_id']}")

    # Bouton de validation
    if st.button(f"Valider préinscription #{p['id']}", key=f"val_{p['id']}"):

        # 1. Cas MEMBRE → inscription automatique
        if p["type"] == "membre" and p["membre_id"] and p["chien_id"] and p["seance_id"]:
            supabase.table("cours_seances_inscriptions").insert({
                "seance_id": p["seance_id"],
                "membre_id": p["membre_id"],
                "chien_id": p["chien_id"],
                "present": False,
                "commentaire": "",
                "actif": True
            }).execute()

            st.success(
                f"Membre validé — inscrit automatiquement à la séance {p['seance_id']}."
            )

        # 2. Cas EXTERIEUR → pas d'inscription automatique
        elif p["type"] == "exterieur":
            st.warning(
                "Extérieur validé — création du membre à l’accueil."
            )

        else:
            st.error("Préinscription invalide ou incomplète.")
            st.stop()

        # 3. Supprimer la préinscription validée
        supabase.table("preinscriptions").delete().eq("id", p["id"]).execute()

        st.info("Préinscription supprimée.")
        st.rerun()
