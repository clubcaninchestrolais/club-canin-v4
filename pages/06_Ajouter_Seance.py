import streamlit as st
from supabase_rest import supabase
from datetime import time, date

st.set_page_config(page_title="Ajouter une séance", page_icon="📅")

st.title("📅 Ajouter une séance")

# ---------------------------------------------------------
# Bouton retour
# ---------------------------------------------------------
if st.button("⬅️ Retour aux cours"):
    st.switch_page("pages/04_Cours.py")

st.markdown("---")

# ---------------------------------------------------------
# Charger la liste des cours
# ---------------------------------------------------------
response = supabase.table("cours").select("*").order("nom").execute()
cours_list = response.data

if not cours_list:
    st.error("Aucun cours disponible. Créez d'abord un type de cours.")
    st.stop()

# ---------------------------------------------------------
# Sélecteur de cours
# ---------------------------------------------------------
cours_noms = {c["nom"]: c["id"] for c in cours_list}
cours_nom_selection = st.selectbox("Sélectionnez un cours", list(cours_noms.keys()))
cours_id = cours_noms[cours_nom_selection]

# ---------------------------------------------------------
# Champs de la séance
# ---------------------------------------------------------
date_seance = st.date_input("Date de la séance", value=date.today())
heure_debut = st.time_input("Heure de début", value=time(9, 0))
heure_fin = st.time_input("Heure de fin", value=time(10, 0))
actif = st.checkbox("Séance active", value=True)

st.markdown("---")

# ---------------------------------------------------------
# Bouton : Créer la séance
# ---------------------------------------------------------
if st.button("➕ Créer la séance"):
    if heure_fin <= heure_debut:
        st.error("L'heure de fin doit être après l'heure de début.")
    else:
        data = {
            "cours_id": cours_id,
            "date_seance": str(date_seance),
            "heure_debut": str(heure_debut),
            "heure_fin": str(heure_fin),
            "actif": actif
        }

        supabase.table("cours_seances").insert(data).execute()
        st.success("Séance créée avec succès !")
