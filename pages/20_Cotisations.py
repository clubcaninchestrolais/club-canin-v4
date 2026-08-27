import streamlit as st

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase
from datetime import datetime, date
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
# Renouvellement = création nouvelle cotisation
# ---------------------------------------------------------
if st.session_state.get("go_renew", False):

    cot = st.session_state["renew_cot"]
    st.session_state["go_renew"] = False

    st.markdown("---")
    st.subheader("🔄 Renouvellement de la cotisation")

    mode_de_paiement = st.selectbox("Mode de paiement", ["cash", "virement", "QRCode"])
    date_paiement = st.date_input("Date de paiement", value=date.today())

    ancienne_echeance = safe_date(cot["date_expiration"]).date()
    nouvelle_date_debut = ancienne_echeance
    nouvelle_expiration = nouvelle_date_debut.replace(year=nouvelle_date_debut.year + 1)

    if st.button("Confirmer le renouvellement"):

        # Création nouvelle cotisation active
        nouvelle = supabase.table("cotisations").insert({
            "membre_id": cot["membre_id"],
            "montant": cot["montant"],
            "type": cot["type"],
            "date_paiement": str(date_paiement),
            "mode_de_paiement": mode_de_paiement,
            "date_expiration": str(nouvelle_expiration),
            "statut": "active",
            "paye": True,
            "remarques": ""
        }).execute()

        nouvelle_id = nouvelle.data[0]["id"]

        # Mettre toutes les anciennes cotisations en historique
        supabase.table("cotisations").update({
            "statut": "historique"
        }).eq("membre_id", cot["membre_id"]).execute()

        # Mettre la nouvelle cotisation en active
        supabase.table("cotisations").update({
            "statut": "active"
        }).eq("id", nouvelle_id).execute()

        st.success("Nouvelle cotisation créée et statut mis à jour.")
        st.rerun()

# ---------------------------------------------------------
# Charger les membres
# ---------------------------------------------------------
membres = supabase.table("membres").select("*").order("nom").execute().data

options = ["-- Tous les membres --"] + [f"{m['nom']} {m['prenom']}" for m in membres]
choix = st.selectbox("Sélectionner un membre", options)

# ---------------------------------------------------------
# Filtre d'affichage
# ---------------------------------------------------------
filtre = st.radio(
    "Afficher",
    ["Toutes les cotisations", "Cotisation active uniquement"],
    horizontal=True
)

st.markdown("---")

# ---------------------------------------------------------
# Charger les cotisations
# ---------------------------------------------------------
cotisations = supabase.table("cotisations").select("*").order("id", desc=True).execute().data

# ---------------------------------------------------------
# Ajouter nom + prénom + sécuriser mode_de_paiement
# ---------------------------------------------------------
for cot in cotisations:
    membre = next((m for m in membres if m["id"] == cot["membre_id"]), None)
    if membre:
        cot["nom"] = membre["nom"]
        cot["prenom"] = membre["prenom"]

    if not cot.get("mode_de_paiement"):
        cot["mode_de_paiement"] = ""

# ---------------------------------------------------------
# Filtrer par membre
# ---------------------------------------------------------
if choix != "-- Tous les membres --":
    nom_sel, prenom_sel = choix.split(" ")
    cotisations = [c for c in cotisations if c["nom"] == nom_sel and c["prenom"] == prenom_sel]

# ---------------------------------------------------------
# Déterminer la cotisation active
# ---------------------------------------------------------
if cotisations:
    cot_sorted = sorted(
        cotisations,
        key=lambda c: safe_date(c["date_expiration"]) or datetime.min,
        reverse=True
    )
    cot_active = cot_sorted[0]["id"]
else:
    cot_active = None

# ---------------------------------------------------------
# Appliquer le filtre d'affichage
# ---------------------------------------------------------
if filtre == "Cotisation active uniquement" and cot_active:
    cotisations = [c for c in cotisations if c["id"] == cot_active]

# ---------------------------------------------------------
# Affichage
# ---------------------------------------------------------
st.subheader("📋 Liste des cotisations")

if cotisations:
    for cot in cotisations:

        date_pay = safe_date(cot.get("date_paiement"))
        date_exp = safe_date(cot.get("date_expiration"))

        # ---------------------------------------------------------
        # Statut automatique
        # ---------------------------------------------------------
        if cot["id"] == cot_active:
            statut = "active"
        elif date_exp and date_exp < datetime.now():
            statut = "expirée"
        else:
            statut = "historique"

        # ---------------------------------------------------------
        # Code couleur
        # ---------------------------------------------------------
        if date_exp:
            jours_restants = (date_exp - datetime.now()).days

            if jours_restants < 0:
                couleur = "#ffcccc"
            elif jours_restants <= 30:
                couleur = "#ffe6cc"
            else:
                couleur = "#e6ffe6" if cot.get("paye") else "#ffffcc"
        else:
            couleur = "#ffcccc"

        # ---------------------------------------------------------
        # Colonnes
        # ---------------------------------------------------------
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([2,2,2,2,2,2,2,2,2])

        with col1:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['nom']}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['prenom']}</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['montant']} €</div>", unsafe_allow_html=True)

        with col4:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{date_pay.strftime('%d/%m/%Y') if date_pay else ''}</div>", unsafe_allow_html=True)

        with col5:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{date_exp.strftime('%d/%m/%Y') if date_exp else ''}</div>", unsafe_allow_html=True)

        with col6:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['mode_de_paiement']}</div>", unsafe_allow_html=True)

        with col7:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{statut}</div>", unsafe_allow_html=True)

        with col8:
            if st.button("Voir détail", key=f"detail_{cot['id']}"):
                st.session_state["cot_id"] = cot["id"]
                st.session_state["go_detail"] = True
                st.rerun()

        with col9:
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
