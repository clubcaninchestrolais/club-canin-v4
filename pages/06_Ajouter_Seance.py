import streamlit as st
from supabase_rest import supabase
from datetime import date

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
note = st.text_area("Note (optionnel)")
actif = st.checkbox("Séance active", value=True)

st.markdown("---")

# ---------------------------------------------------------
# Bouton : Créer la séance
# ---------------------------------------------------------
if st.button("➕ Créer la séance"):

    data = {
        "cours_id": cours_id,
        "date_seance": str(date_seance),
        "note": note if note else None,
        "actif": actif
    }

    try:
        supabase.table("cours_seances").insert(data).execute()
        st.success("Séance créée avec succès !")
    except Exception as e:
        st.error(f"Erreur lors de la création : {e}")

