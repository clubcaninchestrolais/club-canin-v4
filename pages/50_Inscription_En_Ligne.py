import streamlit as st
from supabase_rest import supabase
from datetime import date

st.set_page_config(page_title="Préinscription", page_icon="📝")
st.title("📝 Préinscription à un cours")

# 1. Trouver la prochaine séance
seances = (
    supabase.table("cours_seances")
    .select("*")
    .gte("date_seance", date.today().isoformat())
    .order("date_seance", desc=False)
    .limit(1)
    .execute()
    .data
)

if not seances:
    st.error("Aucune séance future disponible.")
    st.stop()

seance = seances[0]
seance_id = seance["id"]
cours_id = seance["cours_id"]

st.info(f"Séance sélectionnée : {seance['date_seance']} — Cours ID {cours_id}")

# 2. Sélection du membre
membres = (
    supabase.table("membres")
    .select("id, prenom, nom")
    .order("prenom")
    .execute()
    .data
)

choix_membre = st.selectbox(
    "Sélectionner le membre",
    membres,
    format_func=lambda m: f"{m['prenom']} {m['nom']}"
)

membre_id = choix_membre["id"]

# 3. Récupération automatique du chien du membre
chiens = (
    supabase.table("chiens")
    .select("id, nom, race, date_naissance")
    .eq("membre_id", membre_id)
    .execute()
    .data
)

if not chiens:
    st.error("Ce membre n'a aucun chien enregistré.")
    st.stop()

choix_chien = st.selectbox(
    "Sélectionner le chien",
    chiens,
    format_func=lambda c: f"{c['nom']} ({c['race']})"
)

chien_id = choix_chien["id"]
chien_nom = choix_chien["nom"]
chien_race = choix_chien["race"]
chien_naissance = choix_chien["date_naissance"]

# 4. Bouton de confirmation
if st.button("Créer la préinscription membre"):
    supabase.table("preinscriptions").insert({
        "nom": choix_membre["nom"],
        "prenom": choix_membre["prenom"],
        "email": "",
        "telephone": "",
        "chien_nom": chien_nom,
        "chien_race": chien_race,
        "chien_naissance": chien_naissance,
        "cours_id": cours_id,
        "seance_id": seance_id,
        "date_preinscription": date.today().isoformat(),
        "statut": "En attente",
        "traitee": False,
        "acceptee": None,
        "type": "membre",
        "chien_id": chien_id,
        "membre_id": membre_id
    }).execute()

    st.success("Préinscription membre créée avec succès !")
    st.rerun()
