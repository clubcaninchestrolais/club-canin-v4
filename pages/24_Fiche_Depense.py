import streamlit as st
from supabase_rest import supabase
from datetime import datetime

st.set_page_config(page_title="Modifier Dépense", page_icon="✏️")
st.title("✏️ Modifier une dépense")

# Vérifier qu'un ID est présent
if "depense_id" not in st.session_state:
    st.error("Aucune dépense sélectionnée.")
    st.stop()

depense_id = st.session_state["depense_id"]

# Charger la dépense
depense = (
    supabase.table("depenses")
    .select("*")
    .eq("id", depense_id)
    .execute()
    .data
)

if not depense:
    st.error("Dépense introuvable.")
    st.stop()

d = depense[0]

# Formulaire de modification
with st.form("form_modif_depense"):
    date = st.date_input("Date", datetime.strptime(d["date"], "%Y-%m-%d"))
    libelle = st.text_input("Libellé", d["libelle"])
    montant = st.number_input("Montant (€)", min_value=0.0, value=float(d["montant"]), step=0.5)
    rubrique = st.text_input("Rubrique", d["rubrique"])
    remarque = st.text_area("Remarque", d["remarque"] or "")

    submitted = st.form_submit_button("Enregistrer les modifications")

    if submitted:
        supabase.table("depenses").update({
            "date": str(date),
            "libelle": libelle,
            "montant": montant,
            "rubrique": rubrique,
            "remarque": remarque
        }).eq("id", depense_id).execute()

        st.success("Dépense mise à jour.")
        st.page_link("pages/23_Depenses.py")
