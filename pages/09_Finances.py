import streamlit as st
from securite import securite_admin
securite_admin()

from datetime import datetime, date
from supabase_rest import supabase, log_action
from menu import hide_streamlit_menu, menu_lateral


st.set_page_config(page_title="Finances", page_icon="💰")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("Résumé financier du club")

# -----------------------------
# Choix de l'année
# -----------------------------
annee = st.selectbox(
    "Choisir l'année",
    list(range(2020, datetime.now().year + 1)),
    index=(datetime.now().year - 2020)
)

# -----------------------------
# Chargement des données
# -----------------------------
recettes = (
    supabase.table("recettes")
    .select("*")
    .execute()
    .data
)

depenses = (
    supabase.table("depenses")
    .select("*")
    .execute()
    .data
)

# -----------------------------
# Filtre par année
# -----------------------------
recettes_annee = [
    r for r in recettes
    if str(r.get("date", "")).startswith(str(annee))
]

depenses_annee = [
    d for d in depenses
    if str(d.get("date", "")).startswith(str(annee))
]

# -----------------------------
# Totaux sécurisés
# -----------------------------
total_recettes = sum(float(r.get("montant") or 0) for r in recettes_annee)
total_depenses = sum(float(d.get("montant") or 0) for d in depenses_annee)
resultat = total_recettes - total_depenses

# -----------------------------
# Résumé
# -----------------------------
st.subheader(f"Résumé financier {annee}")

col1, col2, col3 = st.columns(3)
col1.metric("Recettes", f"{total_recettes:.2f} €")
col2.metric("Dépenses", f"{total_depenses:.2f} €")
col3.metric("Résultat", f"{resultat:.2f} €")

st.markdown("---")

# -----------------------------
# Détail des recettes
# -----------------------------
st.subheader("Recettes de l'année")

for r in recettes_annee:
    st.write(
        f"📅 {r.get('date', '')} — {r.get('montant', 0)} € — "
        f"{r.get('rubrique', '')} — {r.get('libelle', '')}"
    )

st.markdown("---")

# -----------------------------
# Détail des dépenses
# -----------------------------
st.subheader("Dépenses de l'année")

for d in depenses_annee:
    st.write(
        f"📅 {d.get('date', '')} — {d.get('montant', 0)} € — "
        f"{d.get('rubrique', '')} — {d.get('libelle', '')}"
    )

st.markdown("---")

# -----------------------------
# Clôture de l'année
# -----------------------------
st.subheader("Clôture de l'exercice")

if st.button(f"Clôturer l'année {annee}"):
    supabase.table("finances_clotures").insert({
        "annee": annee,
        "total_recettes": total_recettes,
        "total_depenses": total_depenses,
        "resultat": resultat,
        "date_cloture": datetime.now().isoformat()
    }).execute()

    # 🔍 AUDIT : clôture exercice
    log_action(
        "Clôture exercice",
        f"Année {annee} — résultat {resultat:.2f}€ — utilisateur : {st.session_state.get('username', 'inconnu')}"
    )

    st.success(f"Année {annee} clôturée et enregistrée.")
