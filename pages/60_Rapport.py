import streamlit as st
from securite import securite_admin
securite_admin()

from datetime import datetime
from supabase_rest import supabase

st.title("📊 Rapport du Club – Vue d’ensemble")

st.write("Cette page présente un aperçu général des activités du club.")
st.write("Elle pourra être enrichie avec des graphiques, des statistiques et des analyses détaillées.")

# ---------------------------------------------------------
# Récupération des données (avec protection basique)
# ---------------------------------------------------------

def safe_count(table_name: str, filters: dict | None = None) -> int:
    try:
        q = supabase.table(table_name).select("*")
        if filters:
            for col, val in filters.items():
                q = q.eq(col, val)
        data = q.execute().data
        return len(data) if data else 0
    except Exception:
        return 0

# Membres
nb_membres = safe_count("membres")

# Chiens
nb_chiens = safe_count("chiens")

# Extérieurs (préinscriptions de type "exterieur")
nb_exterieurs = safe_count("preinscriptions", {"type": "exterieur"})

# Cotisations
nb_cotisations = safe_count("cotisations")

# Abonnements
nb_abonnements = safe_count("abonnements")

# Recettes
nb_recettes = safe_count("recettes")

# Dépenses
nb_depenses = safe_count("depenses")

# ---------------------------------------------------------
# Affichage simple
# ---------------------------------------------------------

st.subheader("Résumé rapide")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Membres actifs", nb_membres)
    st.metric("Chiens enregistrés", nb_chiens)

with col2:
    st.metric("Préinscriptions extérieures", nb_exterieurs)
    st.metric("Cotisations actives", nb_cotisations)

with col3:
    st.metric("Abonnements actifs", nb_abonnements)
    st.metric("Nombre de lignes de recettes", nb_recettes)
    st.metric("Nombre de lignes de dépenses", nb_depenses)

st.markdown("---")

st.subheader("Informations complémentaires")

st.write(f"📅 Rapport généré le : **{datetime.now().strftime('%d/%m/%Y à %H:%M')}**")
st.info(
    "Ce rapport est une version simple. "
    "Il pourra être enrichi avec des graphiques, des tendances, des comparaisons mensuelles, "
    "et des analyses détaillées des présences et des finances."
)
