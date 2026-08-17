import streamlit as st
from supabase_rest import supabase
from datetime import datetime

st.set_page_config(page_title="Modifier Recette", page_icon="✏️")
st.title("✏️ Modifier une recette")

# Vérifier qu'un ID est présent
if "recette_id" not in st.session_state:
    st.error("Aucune recette sélectionnée.")
    st.stop()

recette_id = st.session_state["recette_id"]

# Charger la recette
recette = (
    supabase.table("recettes")
    .select("*")
    .eq("id", recette_id)
    .execute()
    .data
)

if not recette:
    st.error("Recette introuvable.")
    st.stop()

r = recette[0]

# Formulaire de modification
with st.form("form_modif_recette"):
    date = st.date_input("Date", datetime.strptime(r["date"], "%Y-%m-%d"))
    libelle = st.text_input("Libellé", r["libelle"])
    montant = st.number_input("Montant (€)", min_value=0.0, value=float(r["montant"]), step=0.5)
    rubrique = st.text_input("Rubrique", r["rubrique"])
    remarque = st.text_area("Remarque", r["remarque"] or "")

    submitted = st.form_submit_button("Enregistrer les modifications")

    if submitted:
        supabase.table("recettes").update({
            "date": str(date),
            "libelle": libelle,
            "montant": montant,
            "rubrique": rubrique,
            "remarque": remarque
        }).eq("id", recette_id).execute()

        st.success("Recette mise à jour.")
        st.page_link("pages/21_Recettes.py")
