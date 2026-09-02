import streamlit as st
from securite import securite_admin
securite_admin()

from datetime import datetime
from supabase_rest import supabase
import pandas as pd
import altair as alt

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="📊 Rapport du Club", page_icon="📊", layout="wide")

st.title("📊 Rapport du Club – Vue d’ensemble")
st.write("Aperçu général des activités du club canin.")

# ---------------------------------------------------------
# FONCTION DE SÉCURITÉ POUR LES COMPTAGES
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

# ---------------------------------------------------------
# RÉCUPÉRATION DES DONNÉES
# ---------------------------------------------------------
nb_membres = safe_count("membres")
nb_chiens = safe_count("chiens")
nb_exterieurs = safe_count("preinscriptions", {"type": "exterieur"})
nb_cotisations = safe_count("cotisations")
nb_abonnements = safe_count("abonnements")
nb_recettes = safe_count("recettes")
nb_depenses = safe_count("depenses")

# ---------------------------------------------------------
# CARTES MODERNES
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
    margin-bottom: 15px;
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
# 📈 GRAPHIQUES
# ---------------------------------------------------------
st.subheader("📈 Graphiques et tendances")

# ---------------------------------------------------------
# 1) Évolution des membres par mois
# ---------------------------------------------------------
try:
    membres_data = supabase.table("membres").select("id", "created_at").execute().data
    df_membres = pd.DataFrame(membres_data)

    df_membres["created_at"] = pd.to_datetime(df_membres["created_at"])
    df_membres["mois"] = df_membres["created_at"].dt.to_period("M").astype(str)

    membres_par_mois = df_membres.groupby("mois").size().reset_index(name="nouveaux_membres")

    chart_membres = (
        alt.Chart(membres_par_mois)
        .mark_line(point=True)
        .encode(
            x="mois",
            y="nouveaux_membres",
            tooltip=["mois", "nouveaux_membres"]
        )
        .properties(title="Évolution des nouveaux membres par mois", height=300)
    )

    st.altair_chart(chart_membres, use_container_width=True)

except Exception:
    st.warning("Impossible d'afficher le graphique des membres.")

# ---------------------------------------------------------
# 2) Répartition des chiens par groupe
# ---------------------------------------------------------
try:
    chiens_data = supabase.table("chiens").select("id", "groupe").execute().data
    df_chiens = pd.DataFrame(chiens_data)

    repartition_chiens = df_chiens.groupby("groupe").size().reset_index(name="total")

    chart_chiens = (
        alt.Chart(repartition_chiens)
        .mark_arc()
        .encode(
            theta="total",
            color="groupe",
            tooltip=["groupe", "total"]
        )
        .properties(title="Répartition des chiens par groupe", height=300)
    )

    st.altair_chart(chart_chiens, use_container_width=True)

except Exception:
    st.warning("Impossible d'afficher le graphique des chiens.")

# ---------------------------------------------------------
# 3) Recettes vs Dépenses
# ---------------------------------------------------------
try:
    recettes_data = supabase.table("recettes").select("id").execute().data
    depenses_data = supabase.table("depenses").select("id").execute().data

    df_finances = pd.DataFrame({
        "Type": ["Recettes", "Dépenses"],
        "Total": [len(recettes_data), len(depenses_data)]
    })

    chart_finances = (
        alt.Chart(df_finances)
        .mark_bar()
        .encode(
            x="Type",
            y="Total",
            color="Type",
            tooltip=["Type", "Total"]
        )
        .properties(title="Comparaison Recettes / Dépenses", height=300)
    )

    st.altair_chart(chart_finances, use_container_width=True)

except Exception:
    st.warning("Impossible d'afficher le graphique des finances.")

# ---------------------------------------------------------
# INFOS COMPLÉMENTAIRES
# ---------------------------------------------------------
st.markdown("---")
st.subheader("ℹ️ Informations complémentaires")

st.write(f"📅 Rapport généré le : **{datetime.now().strftime('%d/%m/%Y à %H:%M')}**")

st.info(
    "Ce tableau de bord modernisé peut être enrichi avec des tendances mensuelles, "
    "des analyses de présences, des graphiques financiers détaillés, "
    "et des statistiques avancées pour les moniteurs."
)
