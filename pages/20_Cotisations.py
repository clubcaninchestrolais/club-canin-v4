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
# Si on revient sur la page sans être en mode renouvellement, on désactive
if "go_renew" in st.session_state and not st.session_state.get("renew_cot"):
    st.session_state["go_renew"] = False


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

    st.markdown("---")

    # ---------------------------------------------------------
    # Encadré bleu : Mode renouvellement actif
    # ---------------------------------------------------------
    st.markdown(
        """
        <div style='padding:15px;border-radius:8px;background-color:#e8f0ff;
                    border-left:6px solid #4a78ff;margin-bottom:15px;'>
        <h3 style='margin:0;'>🔄 Mode renouvellement actif</h3>
        <p style='margin:5px 0 0 0;'>
        Vous êtes en train de renouveler une cotisation.  
        Ne touchez pas au menu “Sélectionner un membre” situé plus bas dans la page.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Renouvellement de la cotisation")

    ancienne_exp = safe_date(cot["date_expiration"]).date()
    nouvelle_date_creation = ancienne_exp
    nouvelle_date_expiration = nouvelle_date_creation.replace(year=nouvelle_date_creation.year + 1)

    # ---------------------------------------------------------
    # Résumé clair du renouvellement
    # ---------------------------------------------------------
    st.markdown(
        f"""
        <div style='padding:15px;border-radius:8px;background-color:#f0f4ff;
                    border:1px solid #c7d4ff;margin-bottom:20px;'>
        <h4 style='margin-top:0;'>📘 Résumé du renouvellement</h4>
        <ul>
            <li><b>Ancienne expiration :</b> {ancienne_exp.strftime('%d/%m/%Y')}</li>
            <li><b>Nouvelle date de création :</b> {nouvelle_date_creation.strftime('%d/%m/%Y')}</li>
            <li><b>Nouvelle expiration :</b> {nouvelle_date_expiration.strftime('%d/%m/%Y')}</li>
            <li><b>Montant :</b> {cot['montant']} €</li>
            <li><b>Statut final :</b> active</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Paiement du renouvellement")

    mode_de_paiement = st.selectbox("Mode de paiement", ["cash", "virement", "QRCode"])
    date_paiement = st.date_input("Date de paiement", value=None)

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

        st.session_state["go_renew"] = False

        st.success("Renouvellement effectué.")
        st.rerun()

    # ---------------------------------------------------------
    # Encadré jaune : avertissement
    # ---------------------------------------------------------
    st.markdown(
        """
        <div style='margin-top:20px;padding:12px;background:#fff3cd;
                    border-left:6px solid #ffca2c;border-radius:4px;'>
        ⚠️ <b>Important :</b> Pendant un renouvellement, ignorez le menu “Sélectionner un membre”
        situé plus bas.  
        Il n’a aucun effet sur le renouvellement.
        </div>
        """,
        unsafe_allow_html=True
    )

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

    header_cols = st.columns([2,2,2,2,2,2,2,2,2])
    with header_cols[0]: st.markdown("**Nom**")
    with header_cols[1]: st.markdown("**Prénom**")
    with header_cols[2]: st.markdown("**Montant**")
    with header_cols[3]: st.markdown("**Création**")
    with header_cols[4]: st.markdown("**Expiration**")
    with header_cols[5]: st.markdown("**Paiement**")
    with header_cols[6]: st.markdown("**Statut**")
    with header_cols[7]: st.markdown("**Détail**")
    with header_cols[8]: st.markdown("**Renouveler**")

    st.markdown("---")

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

        cols = st.columns([2,2,2,2,2,2,2,2,2])

        with cols[0]:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['nom']}</div>", unsafe_allow_html=True)

        with cols[1]:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['prenom']}</div>", unsafe_allow_html=True)

        with cols[2]:
            st.markdown(f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{cot['montant']} €</div>", unsafe_allow_html=True)

        with cols[3]:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{date_creation.strftime('%d/%m/%Y') if date_creation else ''}</div>",
                unsafe_allow_html=True
            )

        with cols[4]:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{date_exp.strftime('%d/%m/%Y') if date_exp else ''}</div>",
                unsafe_allow_html=True
            )

        with cols[5]:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{date_pay.strftime('%d/%m/%Y') if date_pay else ''}</div>",
                unsafe_allow_html=True
            )

        with cols[6]:
            etat_paiement = "payée" if paye else "non payée"
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>{statut} ({etat_paiement})</div>",
                unsafe_allow_html=True
            )

        with cols[7]:
            if st.button("Voir détail", key=f"detail_{cot['id']}"):
                st.session_state["cot_id"] = cot["id"]
                st.session_state["go_detail"] = True
                st.rerun()

        with cols[8]:
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
