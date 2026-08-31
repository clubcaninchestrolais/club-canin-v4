import streamlit as st
from securite import securite_user
securite_user()

from datetime import datetime, date
from supabase_rest import supabase
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
    if isinstance(value, str):
        v = value.strip()
        if v == "":
            return None
        try:
            return datetime.fromisoformat(v.replace("Z", "").replace("T", " "))
        except:
            pass
        try:
            return datetime.strptime(v, "%Y-%m-%d")
        except:
            pass
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
    date_paiement = st.date_input("Date de paiement", value=None)

    ancienne_exp = safe_date(cot["date_expiration"]).date()

    # LOGIQUE VALIDÉE PAR TOI :
    # date_creation = date_expiration de l’ancienne cotisation
    nouvelle_date_creation = ancienne_exp
    nouvelle_date_expiration = nouvelle_date_creation.replace(year=nouvelle_date_creation.year + 1)

    if st.button("Confirmer le renouvellement"):

        nouvelle = supabase.table("cotisations").insert({
            "membre_id": cot["membre_id"],
            "montant": cot["montant"],
            "date_creation": str(nouvelle_date_creation),
            "date_expiration": str(nouvelle_date_expiration),
            "date_paiement": str(date_paiement) if date_paiement else None,
            "mode_de_paiement": mode_de_paiement if date_paiement else None,
            "statut": "active",
            "paye": bool(date_paiement),
            "remarques": ""
        }).execute()

        nouvelle_id = nouvelle.data[0]["id"]

        supabase.table("cotisations").update({
            "statut": "historique"
        }).eq("membre_id", cot["membre_id"]).execute()

        supabase.table("cotisations").update({
            "statut": "active"
        }).eq("id", nouvelle_id).execute()

        st.success("Renouvellement effectué.")
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
# Mise à jour automatique du statut selon la date d'expiration
# ---------------------------------------------------------
today = datetime.today().date()

for cot in cotisations:
    exp = safe_date(cot["date_expiration"])
    if not exp:
        continue

    if exp.date() < today and cot["statut"] != "expirée":
        supabase.table("cotisations").update({"statut": "expirée"}).eq("id", cot["id"]).execute()
        cot["statut"] = "expirée"

    elif exp.date() >= today and cot["statut"] == "expirée":
        supabase.table("cotisations").update({"statut": "active"}).eq("id", cot["id"]).execute()
        cot["statut"] = "active"

# ---------------------------------------------------------
# Ajouter nom + prénom
# ---------------------------------------------------------
for cot in cotisations:
    membre = next((m for m in membres if m["id"] == cot["membre_id"]), None)
    if membre:
        cot["nom"] = membre["nom"]
        cot["prenom"] = membre["prenom"]

    if not cot.get("mode_de_paiement"):
        cot["mode_de_paiement"] = ""

# Filtrer par membre
if choix != "-- Tous les membres --":
    nom_sel, prenom_sel = choix.split(" ")
    cotisations = [c for c in cotisations if c["nom"] == nom_sel and c["prenom"] == prenom_sel]

# Filtre actif uniquement
if filtre == "Cotisation active uniquement":
    cotisations = [c for c in cotisations if c["statut"] == "active"]

# ---------------------------------------------------------
# Affichage
# ---------------------------------------------------------
st.subheader("📋 Liste des cotisations")

if cotisations:
    for cot in cotisations:

        date_creation = safe_date(cot.get("date_creation"))
        date_pay = safe_date(cot.get("date_paiement"))
        date_exp = safe_date(cot.get("date_expiration"))

        statut = cot["statut"]
        paye = cot.get("paye", False)

        statut_normalise = statut.lower().strip().replace("é", "e").replace("è", "e")

        if statut_normalise == "active":
            couleur = "#e6ffe6" if paye else "#ffe6b3"
        elif statut_normalise == "expiree":
            couleur = "#ffcccc"
        elif statut_normalise == "gratuit":
            couleur = "#cce6ff"
        else:
            couleur = "#ffffcc"

        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([2,2,2,2,2,2,2,2,2])

        with col1:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['nom']}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['prenom']}</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['montant']} €</div>", unsafe_allow_html=True)

        with col4:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{date_creation.strftime('%d/%m/%Y') if date_creation else ''}</div>",
                unsafe_allow_html=True
            )

        with col5:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{date_exp.strftime('%d/%m/%Y') if date_exp else ''}</div>",
                unsafe_allow_html=True
            )

        with col6:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{date_pay.strftime('%d/%m/%Y') if date_pay else ''}</div>",
                unsafe_allow_html=True
            )

        with col7:
            etat_paiement = "payée" if paye else "non payée"
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{statut} ({etat_paiement})</div>",
                unsafe_allow_html=True
            )

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

# ---------------------------------------------------------
# SECTION CRÉATION COTISATION (FLUX 1)
# ---------------------------------------------------------
st.markdown("---")
st.subheader("➕ Création cotisation nouveau membre")

if choix == "-- Tous les membres --":
    st.info("Sélectionnez un membre pour créer une cotisation.")
else:
    montant = st.number_input("Montant (€)", min_value=0, value=45)
    date_paiement = st.date_input("Date de paiement", value=None)
    mode = st.selectbox("Mode de paiement", ["", "cash", "virement", "QRCode"])

    if st.button("Créer la cotisation"):
        membre_id = next(m["id"] for m in membres if f"{m['nom']} {m['prenom']}" == choix)

        date_creation = date.today()
        date_expiration = date_creation.replace(year=date_creation.year + 1)

        supabase.table("cotisations").update({
            "statut": "historique"
        }).eq("membre_id", membre_id).execute()

        supabase.table("cotisations").insert({
            "membre_id": membre_id,
            "montant": montant,
            "date_creation": str(date_creation),
            "date_expiration": str(date_expiration),
            "date_paiement": str(date_paiement) if date_paiement else None,
            "mode_de_paiement": mode if date_paiement else None,
            "statut": "active",
            "paye": bool(date_paiement),
            "remarques": ""
        }).execute()

        st.success("Cotisation créée.")
        st.rerun()
