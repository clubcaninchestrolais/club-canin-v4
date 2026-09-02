import streamlit as st
from securite import securite_admin
securite_admin()

from datetime import datetime
from supabase_rest import supabase

st.set_page_config(page_title="📊 Rapport du Club", page_icon="📊", layout="wide")

st.title("📊 Rapport du Club – Vue d’ensemble")
st.write("Aperçu général des activités du club canin.")

# ---------------------------------------------------------
# Récupération des données
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

nb_membres = safe_count("membres")
nb_chiens = safe_count("chiens")
nb_exterieurs = safe_count("preinscriptions", {"type": "exterieur"})
nb_cotisations = safe_count("cotisations")
nb_abonnements = safe_count("abonnements")
nb_recettes = safe_count("recettes")
nb_depenses = safe_count("depenses")

# ---------------------------------------------------------
# Cartes modernes
# ---------------------------------------------------------

st.subheader("📌 Résumé rapide")

card_css = """
<style>
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f7f9fc;
    border: 1px solid #e3e6eb;
    text-align: center;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}
.card h2 {
    font-size: 32px;
    margin: 0;
    color: #003366;
}
.card p {
    font-size: 18px;
    margin: 0;
    color: #555;
}
</style>
"""
st.markdown(card_css, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="card">
            <h2>👥 {nb_membres}</h2>
            <p>Membres actifs</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card">
            <h2>🐶 {nb_chiens}</h2>
            <p>Chiens enregistrés</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="card">
            <h2>🌐 {nb_exterieurs}</h2>
            <p>Préinscriptions extérieures</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card">
            <h2>💳 {nb_cotisations}</h2>
            <p>Cotisations actives</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="card">
            <h2>🎫 {nb_abonnements}</h2>
            <p>Abonnements actifs</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card">
            <h2>📈 {nb_recettes}</h2>
            <p>Lignes de recettes</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card">
            <h2>🧾 {nb_depenses}</h2>
            <p>Lignes de dépenses</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------
# Informations complémentaires
# ---------------------------------------------------------

st.subheader("ℹ️ Informations complémentaires")

st.write(f"📅 Rapport généré le : **{datetime.now().strftime('%d/%m/%Y à %H:%M')}**")

st.info(
    "Ce tableau de bord est désormais modernisé. "
    "Il peut être enrichi avec des graphiques, des tendances mensuelles, "
    "et des analyses détaillées des présences et des finances."
)
