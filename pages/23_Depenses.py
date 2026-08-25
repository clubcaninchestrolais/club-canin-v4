import streamlit as st
from supabase_rest import supabase
from datetime import datetime
from menu import hide_streamlit_menu, menu_lateral

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Dépenses", page_icon="📉", layout="wide")

# --- MENU PERSONNALISÉ ---
hide_streamlit_menu()
menu_lateral()

st.title("📉 Dépenses du club")

# Charger les dépenses
depenses = (
    supabase.table("depenses")
    .select("*")
    .order("date", desc=True)
    .execute()
    .data
)

# ---------------------------------------------------------
# Ajouter une dépense
# ---------------------------------------------------------

st.subheader("Ajouter une dépense")

with st.form("add_depense"):
    date = st.date_input("Date")
    rubrique = st.text_input("Rubrique")
    libelle = st.text_input("Libellé")
    montant = st.number_input("Montant (€)", min_value=0.0, step=0.5)
    remarque = st.text_input("Remarque")
    exercice = date.year

    submitted = st.form_submit_button("Ajouter")
    if submitted:
        supabase.table("depenses").insert({
            "date": date.isoformat(),
            "rubrique": rubrique,
            "libelle": libelle,
            "montant": montant,
            "remarque": remarque,
            "exercice": exercice
        }).execute()
        st.success("Dépense ajoutée")
        st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Liste + Modifier + Supprimer
# ---------------------------------------------------------

st.subheader("Liste des dépenses")

for d in depenses:
    col1, col2, col3 = st.columns([6, 1, 1])

    col1.write(
        f"📅 {d.get('date', '')} — {d.get('montant', 0)} € — "
        f"{d.get('rubrique', '')} — {d.get('libelle', '')}"
    )

    if col2.button("✏️", key=f"edit_depense_{d['id']}"):
        st.session_state["edit_depense"] = d

    if col3.button("🗑️", key=f"del_depense_{d['id']}"):
        supabase.table("depenses").delete().eq("id", d["id"]).execute()
        st.rerun()

# ---------------------------------------------------------
# Fenêtre de modification
# ---------------------------------------------------------

if "edit_depense" in st.session_state:
    d = st.session_state["edit_depense"]

    st.markdown("### Modifier la dépense")

    with st.form("form_edit_depense"):
        new_date = st.date_input("Date", datetime.fromisoformat(d["date"]))
        new_rubrique = st.text_input("Rubrique", d.get("rubrique", ""))
        new_libelle = st.text_input("Libellé", d.get("libelle", ""))
        new_montant = st.number_input("Montant (€)", value=float(d.get("montant") or 0))
        new_remarque = st.text_input("Remarque", d.get("remarque", ""))

        submitted = st.form_submit_button("Enregistrer")
        if submitted:
            supabase.table("depenses").update({
                "date": new_date.isoformat(),
                "rubrique": new_rubrique,
                "libelle": new_libelle,
                "montant": new_montant,
                "remarque": new_remarque,
                "exercice": new_date.year
            }).eq("id", d["id"]).execute()

            del st.session_state["edit_depense"]
            st.success("Dépense modifiée")
            st.rerun()
