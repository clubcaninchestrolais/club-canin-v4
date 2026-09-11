import streamlit as st
from securite import securite_admin
securite_admin()

from datetime import datetime
from supabase_rest import supabase
import pandas as pd
import altair as alt
from fpdf import FPDF
import io

from menu import hide_streamlit_menu, menu_lateral

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="📊 Rapport du Club", page_icon="📊", layout="wide")
hide_streamlit_menu()
menu_lateral()

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
# 💰 SYNTHÈSE FINANCIÈRE
# ---------------------------------------------------------
st.subheader("💰 Synthèse financière")

try:
    recettes_data = supabase.table("recettes").select("montant").execute().data
    depenses_data = supabase.table("depenses").select("montant").execute().data

    total_recettes = sum([r["montant"] for r in recettes_data]) if recettes_data else 0
    total_depenses = sum([d["montant"] for d in depenses_data]) if depenses_data else 0
    solde = total_recettes - total_depenses

    colA, colB, colC = st.columns(3)
    colA.metric("Total des recettes", f"{total_recettes:.2f} €")
    colB.metric("Total des dépenses", f"{total_depenses:.2f} €")
    colC.metric("Solde du club", f"{solde:.2f} €")

except Exception:
    st.warning("Impossible de calculer la synthèse financière.")

st.markdown("---")

# ---------------------------------------------------------
# 📈 GRAPHIQUES
# ---------------------------------------------------------
st.subheader("📈 Graphiques et tendances")

# ---------------------------------------------------------
# 1) Évolution des membres par mois
# ---------------------------------------------------------
try:
    membres_data = supabase.table("membres").select("*").execute().data
    df_membres = pd.DataFrame(membres_data)

    df_membres["date"] = pd.to_datetime(df_membres.get("created_at", df_membres.get("date_inscription")))
    df_membres["mois"] = df_membres["date"].dt.to_period("M").astype(str)

    membres_par_mois = df_membres.groupby("mois").size().reset_index(name="nouveaux_membres")

    chart_membres = (
        alt.Chart(membres_par_mois)
        .mark_line(point=True)
        .encode(x="mois", y="nouveaux_membres", tooltip=["mois", "nouveaux_membres"])
        .properties(title="Évolution des nouveaux membres par mois", height=300)
    )

    st.altair_chart(chart_membres, use_container_width=True)

except Exception:
    st.warning("Impossible d'afficher le graphique des membres.")

# ---------------------------------------------------------
# 2) Répartition des chiens par groupe
# ---------------------------------------------------------
try:
    chiens_data = supabase.table("chiens").select("*").execute().data
    df_chiens = pd.DataFrame(chiens_data)

    df_chiens["groupe"] = df_chiens["groupe"].fillna("Non défini")

    repartition_chiens = df_chiens.groupby("groupe").size().reset_index(name="total")

    chart_chiens = (
        alt.Chart(repartition_chiens)
        .mark_arc()
        .encode(theta="total", color="groupe", tooltip=["groupe", "total"])
        .properties(title="Répartition des chiens par groupe", height=300)
    )

    st.altair_chart(chart_chiens, use_container_width=True)

except Exception:
    st.warning("Impossible d'afficher le graphique des chiens.")

# ---------------------------------------------------------
# 3) Présences par mois
# ---------------------------------------------------------
st.subheader("📅 Présences par mois")

try:
    pres_data = supabase.table("presences").select("created_at").execute().data
    df_pres = pd.DataFrame(pres_data)

    df_pres["date"] = pd.to_datetime(df_pres["created_at"])
    df_pres["mois"] = df_pres["date"].dt.to_period("M").astype(str)

    pres_par_mois = df_pres.groupby("mois").size().reset_index(name="total")

    chart_pres_mois = (
        alt.Chart(pres_par_mois)
        .mark_line(point=True)
        .encode(x="mois", y="total", tooltip=["mois", "total"])
        .properties(title="Évolution des présences par mois", height=300)
    )

    st.altair_chart(chart_pres_mois, use_container_width=True)

except Exception:
    st.warning("Impossible d'afficher les présences mensuelles.")

# ---------------------------------------------------------
# 4) Présences du jour
# ---------------------------------------------------------
st.subheader("👣 Présences du jour")

try:
    today = datetime.now().strftime("%Y-%m-%d")

    seances = (
        supabase.table("cours_seances")
        .select("id", "date_seance")
        .eq("date_seance", today)
        .execute()
        .data
    )

    if not seances:
        st.info("Aucune séance aujourd’hui.")
    else:
        seance_ids = [s["id"] for s in seances]

        presences = (
            supabase.table("presences")
            .select("id", "seance_id")
            .in_("seance_id", seance_ids)
            .execute()
            .data
        )

        df_pres = pd.DataFrame(presences)

        if df_pres.empty:
            st.info("Aucune présence enregistrée aujourd’hui.")
        else:
            df_pres["seance_id"] = df_pres["seance_id"].astype(str)
            presences_par_seance = df_pres.groupby("seance_id").size().reset_index(name="total")

            chart_presences = (
                alt.Chart(presences_par_seance)
                .mark_bar()
                .encode(x="seance_id", y="total", tooltip=["seance_id", "total"], color="total")
                .properties(title="Présences du jour par séance", height=300)
            )

            st.altair_chart(chart_presences, use_container_width=True)

except Exception:
    st.warning("Impossible d'afficher le graphique des présences du jour.")

# ---------------------------------------------------------
# 📄 EXPORT PDF DU RAPPORT
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📄 Export PDF du rapport")

def safe_text(txt):
    """Remplace les caractères non compatibles FPDF."""
    replacements = {
        "€": "EUR", "é": "e", "è": "e", "ê": "e", "à": "a", "ç": "c",
        "ô": "o", "ù": "u", "î": "i", "ï": "i", "É": "E", "È": "E",
        "Ç": "C", "—": "-", "…": "..."
    }
    for bad, good in replacements.items():
        txt = txt.replace(bad, good)
    return txt

if st.button("Générer le PDF du rapport"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=safe_text("Rapport du club canin"), ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt=safe_text("Indicateurs principaux :"), ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, txt=safe_text(f"Membres actifs : {nb_membres}"), ln=True)
    pdf.cell(200, 8, txt=safe_text(f"Chiens enregistres : {nb_chiens}"), ln=True)
    pdf.cell(200, 8, txt=safe_text(f"Preinscriptions exterieures : {nb_exterieurs}"), ln=True)
    pdf.cell(200, 8, txt=safe_text(f"Cotisations actives : {nb_cotisations}"), ln=True)
    pdf.cell(200, 8, txt=safe_text(f"Abonnements actifs : {nb_abonnements}"), ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt=safe_text("Synthese financiere :"), ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, txt=safe_text(f"Total recettes : {total_recettes:.2f} EUR"), ln=True)
    pdf.cell(200, 8, txt=safe_text(f"Total depenses : {total_depenses:.2f} EUR"), ln=True)
    pdf.cell(200, 8, txt=safe_text(f"Solde du club : {solde:.2f} EUR"), ln=True)

    buffer = io.BytesIO()
    pdf.output(buffer)
    pdf_bytes = buffer.getvalue()

    st.download_button(
        label="📥 Télécharger le PDF",
        data=pdf_bytes,
        file_name="rapport_club.pdf",
        mime="application/pdf"
    )

# ---------------------------------------------------------
# INFOS COMPLÉMENTAIRES
# ---------------------------------------------------------
st.markdown("---")
st.subheader("ℹ️ Informations complémentaires")
st.write(f"📅 Rapport généré le : **{datetime.now().strftime('%d/%m/%Y à %H:%M')}**")
