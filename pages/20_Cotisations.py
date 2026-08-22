import streamlit as st
from supabase_rest import supabase
from datetime import datetime, date

st.set_page_config(page_title="Cotisations", page_icon="💳")
st.title("💳 Gestion des cotisations")

# ---------------------------------------------------------
# Retour fiable depuis la fiche cotisation
# ---------------------------------------------------------
if st.session_state.get("go_back", False):
    st.session_state["go_back"] = False
    st.session_state["cot_id"] = None

    # Remonter en haut de la page
    if st.session_state.get("scroll_top", False):
        st.session_state["scroll_top"] = False
        st.markdown("<script>window.scrollTo(0, 0);</script>", unsafe_allow_html=True)

    st.rerun()

# ---------------------------------------------------------
# Fonction de conversion sécurisée
# ---------------------------------------------------------
def safe_date(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, str) and value.strip() != "":
        try:
            return datetime.fromisoformat(value.replace("Z", ""))
        except:
            return None
    return None

# ---------------------------------------------------------
# Charger les membres
# ---------------------------------------------------------
membres = (
    supabase.table("membres")
    .select("*")
    .order("nom")
    .execute()
    .data
)

options = ["-- Tous les membres --"] + [
    f"{m['nom']} {m['prenom']}" for m in membres
]

choix = st.selectbox("Sélectionner un membre", options)

st.markdown("---")

# ---------------------------------------------------------
# Charger les cotisations
# ---------------------------------------------------------
cotisations = (
    supabase.table("cotisations")
    .select("*")
    .order("id", desc=True)
    .execute()
    .data
)

# Ajouter nom + prénom
for cot in cotisations:
    membre = next((m for m in membres if m["id"] == cot["membre_id"]), None)
    if membre:
        cot["nom"] = membre["nom"]
        cot["prenom"] = membre["prenom"]

# Filtrer si un membre est sélectionné
if choix != "-- Tous les membres --":
    nom_sel, prenom_sel = choix.split(" ")
    cotisations = [
        c for c in cotisations
        if c["nom"] == nom_sel and c["prenom"] == prenom_sel
    ]

# ---------------------------------------------------------
# Affichage ultra-compact avec couleur impayés
# ---------------------------------------------------------
st.subheader("📋 Liste des cotisations")

if cotisations:
    for cot in cotisations:

        date_pay = safe_date(cot.get("date_paiement"))
        date_exp = safe_date(cot.get("date_expiration"))

        # Couleur selon paiement / échéance
        if cot.get("paye"):
            couleur = "#e6ffe6"  # vert = payé
        else:
            if date_exp:
                jours_restants = (date_exp - datetime.now()).days
                if jours_restants < 0:
                    couleur = "#ffcccc"
                elif jours_restants <= 30:
                    couleur = "#ffe6cc"
                else:
                    couleur = "#ffcccc"
            else:
                couleur = "#ffcccc"

        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])

        with col1:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>"
                f"{cot.get('nom', '')}</div>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>"
                f"{cot.get('prenom', '')}</div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>"
                f"{cot.get('montant', 0)} €</div>",
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>"
                f"{date_pay.strftime('%d/%m/%Y') if date_pay else ''}</div>",
                unsafe_allow_html=True
            )

        with col5:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>"
                f"{date_exp.strftime('%d/%m/%Y') if date_exp else ''}</div>",
                unsafe_allow_html=True
            )

        with col6:
            if st.button("Voir détail", key=f"detail_{cot['id']}"):
                st.session_state["cot_id"] = cot["id"]
                st.session_state["go_detail"] = True
                st.rerun()

else:
    st.info("Aucune cotisation trouvée.")

# ---------------------------------------------------------
# Navigation vers fiche détail (FIABLE)
# ---------------------------------------------------------
if st.session_state.get("go_detail", False):
    st.session_state["go_detail"] = False
    st.switch_page("20_Cotisation")  # nom exact de ta fiche cotisation


