import streamlit as st
from supabase_rest import supabase
from datetime import datetime, date

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from menu import hide_streamlit_menu, menu_lateral

st.set_page_config(page_title="Cotisations", page_icon="💳", layout="wide")
hide_streamlit_menu()
menu_lateral()

st.title("💳 Gestion des cotisations")

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
membres = supabase.table("membres").select("*").order("nom").execute().data

options = ["-- Tous les membres --"] + [
    f"{m['nom']} {m['prenom']}" for m in membres
]

choix = st.selectbox("Sélectionner un membre", options)
st.markdown("---")

# ---------------------------------------------------------
# Charger les cotisations
# ---------------------------------------------------------
raw_cot = supabase.table("cotisations").select("*").order("id", desc=True).execute().data

# ---------------------------------------------------------
# Reconstruction propre
# ---------------------------------------------------------
cotisations = []
for cot in raw_cot:

    membre = next((m for m in membres if m["id"] == cot["membre_id"]), None)
    cot["nom"] = membre["nom"] if membre else ""
    cot["prenom"] = membre["prenom"] if membre else ""

    if cot.get("mode_de_paiement") is None:
        cot["mode_de_paiement"] = ""

    cotisations.append(cot)

# ---------------------------------------------------------
# Filtrer si un membre est sélectionné
# ---------------------------------------------------------
if choix != "-- Tous les membres --":
    nom_sel, prenom_sel = choix.split(" ")
    cotisations = [
        c for c in cotisations
        if c["nom"] == nom_sel and c["prenom"] == prenom_sel
    ]

# ---------------------------------------------------------
# AFFICHAGE
# ---------------------------------------------------------
st.subheader("📋 Liste des cotisations")

if cotisations:
    for cot in cotisations:

        date_pay = safe_date(cot.get("date_paiement"))
        date_exp = safe_date(cot.get("date_expiration"))

        # ---------------------------------------------------------
        # BADGES
        # ---------------------------------------------------------
        badge_paye = (
            "<span style='background:#c8f7c5;padding:3px;border-radius:4px;'>Payé</span>"
            if cot.get("paye") else
            "<span style='background:#f7c5c5;padding:3px;border-radius:4px;'>Impayé</span>"
        )

        if date_exp:
            jours = (date_exp - datetime.now()).days
            if jours < 0:
                badge_exp = "<span style='background:#ff9999;padding:3px;border-radius:4px;'>Expirée</span>"
                couleur = "#ffcccc"
            elif jours <= 30:
                badge_exp = "<span style='background:#ffd699;padding:3px;border-radius:4px;'>Bientôt expirée</span>"
                couleur = "#ffe6cc"
            else:
                badge_exp = "<span style='background:#c8f7c5;padding:3px;border-radius:4px;'>Valide</span>"
                couleur = "#e6ffe6"
        else:
            badge_exp = "<span style='background:#ff9999;padding:3px;border-radius:4px;'>Erreur date</span>"
            couleur = "#ffcccc"

        # ---------------------------------------------------------
        # Colonnes
        # ---------------------------------------------------------
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2,2,2,2,2,2,2,2])

        with col1:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['nom']}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['prenom']}</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['montant']} €</div>", unsafe_allow_html=True)

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
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['mode_de_paiement']}</div>",
                unsafe_allow_html=True
            )

        with col7:
            st.markdown(badge_paye, unsafe_allow_html=True)

        with col8:
            st.markdown(badge_exp, unsafe_allow_html=True)

        # Boutons
        if st.button("Voir détail", key=f"detail_{cot['id']}"):
            st.session_state["cot_id"] = cot["id"]
            st.session_state["go_detail"] = True
            st.rerun()

        if st.button("Renouveler", key=f"renew_{cot['id']}"):
            st.session_state["renew_cot"] = cot
            st.session_state["go_renew"] = True
            st.rerun()

else:
    st.info("Aucune cotisation trouvée.")

# ---------------------------------------------------------
# Navigation vers fiche détail
# ---------------------------------------------------------
if st.session_state.get("go_detail", False):
    st.session_state["go_detail"] = False
    st.switch_page("pages/32_Fiche_Cotisation.py")
