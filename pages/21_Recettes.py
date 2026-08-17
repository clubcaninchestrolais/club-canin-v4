import streamlit as st
from supabase_rest import supabase
from datetime import datetime

st.set_page_config(page_title="Recettes", page_icon="💵")

st.title("Recettes du club")

# ---------------------------------------------------------
# Chargement des données
# ---------------------------------------------------------

recettes = (
    supabase.table("recettes")
    .select("*")
    .order("date", desc=True)
    .execute()
    .data
)

# ---------------------------------------------------------
# Ajouter une recette
# ---------------------------------------------------------

st.subheader("Ajouter une recette")

with st.form("add_recette"):
    date = st.date_input("Date")
    rubrique = st.text_input("Rubrique")
    libelle = st.text_input("Libellé")
    montant = st.number_input("Montant (€)", min_value=0.0, step=0.5)
    remarque = st.text_input("Remarque")
    exercice = date.year

    submitted = st.form_submit_button("Ajouter")
    if submitted:
        supabase.table("recettes").insert({
            "date": date.isoformat(),
            "rubrique": rubrique,
            "libelle": libelle,
            "montant": montant,
            "remarque": remarque,
            "exercice": exercice
        }).execute()
        st.success("Recette ajoutée")
        st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Liste + Modifier + Supprimer
# ---------------------------------------------------------

st.subheader("Liste des recettes")

for r in recettes:
    col1, col2, col3 = st.columns([6, 1, 1])

    col1.write(
        f"📅 {r.get('date', '')} — {r.get('montant', 0)} € — "
        f"{r.get('rubrique', '')} — {r.get('libelle', '')}"
    )

    # Bouton modifier
    if col2.button("✏️", key=f"edit_recette_{r['id']}"):
        st.session_state["edit_recette"] = r

    # Bouton supprimer
    if col3.button("🗑️", key=f"del_recette_{r['id']}"):
        supabase.table("recettes").delete().eq("id", r["id"]).execute()
        st.rerun()

# ---------------------------------------------------------
# Fenêtre de modification
# ---------------------------------------------------------

if "edit_recette" in st.session_state:
    r = st.session_state["edit_recette"]

    st.markdown("### Modifier la recette")

    with st.form("form_edit_recette"):
        new_date = st.date_input("Date", datetime.fromisoformat(r["date"]))
        new_rubrique = st.text_input("Rubrique", r.get("rubrique", ""))
        new_libelle = st.text_input("Libellé", r.get("libelle", ""))
        new_montant = st.number_input("Montant (€)", value=float(r.get("montant") or 0))
        new_remarque = st.text_input("Remarque", r.get("remarque", ""))

        submitted = st.form_submit_button("Enregistrer")
        if submitted:
            supabase.table("recettes").update({
                "date": new_date.isoformat(),
                "rubrique": new_rubrique,
                "libelle": new_libelle,
                "montant": new_montant,
                "remarque": new_remarque,
                "exercice": new_date.year
            }).eq("id", r["id"]).execute()

            del st.session_state["edit_recette"]
            st.success("Recette modifiée")
            st.rerun()
