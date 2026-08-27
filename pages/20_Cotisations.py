import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase
from datetime import datetime, date
from menu import hide_streamlit_menu, menu_lateral

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Cotisations", page_icon="💳", layout="wide")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
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

# ---------------------------------------------------------
# Ajouter nom + prénom + sécuriser mode_de_paiement
# ---------------------------------------------------------
for cot in cotisations:
    membre = next((m for m in membres if m["id"] == cot["membre_id"]), None)
    if membre:
        cot["nom"] = membre["nom"]
        cot["prenom"] = membre["prenom"]

    # ⭐ Correction : garantir que la clé existe pour l'affichage
    if "mode_de_paiement" not in cot or cot["mode_de_paiement"] is None:
        cot["mode_de_paiement"] = ""

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
                    couleur = "#ffcccc"  # rouge = expirée impayée
                elif jours_restants <= 30:
                    couleur = "#ffe6cc"  # orange = bientôt expirée impayée
                else:
                    couleur = "#ffcccc"
            else:
                couleur = "#ffcccc"

        # 8 colonnes pour inclure le mode de paiement
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2, 2, 2, 2, 2, 2, 2, 2])

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

        # ⭐ MODE DE PAIEMENT — enfin visible !
        with col6:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>"
                f"{cot.get('mode_de_paiement', '')}</div>",
                unsafe_allow_html=True
            )

        with col7:
            if st.button("Voir détail", key=f"detail_{cot['id']}"):
                st.session_state["cot_id"] = cot["id"]
                st.session_state["go_detail"] = True
                st.rerun()

        with col8:
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
# Renouvellement d’une cotisation
# ---------------------------------------------------------
if st.session_state.get("go_renew", False):

    cot = st.session_state["renew_cot"]
    st.session_state["go_renew"] = False

    st.markdown("---")
    st.subheader("🔄 Renouvellement de la cotisation")

    mode_de_paiement = st.selectbox(
        "Mode de paiement",
        ["cash", "virement", "QRCode"]
    )

    date_paiement = st.date_input(
        "Date de paiement",
        value=date.today(),
        help="Encoder la date du paiement"
    )

    ancienne_echeance = safe_date(cot["date_expiration"])
    nouvelle_echeance = ancienne_echeance.replace(
        year=ancienne_echeance.year + 1
    )

    if st.button("Confirmer le renouvellement"):
        supabase.table("cotisations").update({
            "date_paiement": str(date_paiement),
            "mode_de_paiement": mode_de_paiement,
            "date_expiration": str(nouvelle_echeance),
            "paye": True,
            "statut": "renouvelée"
        }).eq("id", cot["id"]).execute()

        st.success("Cotisation renouvelée avec succès.")
        st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Création d’une cotisation
# ---------------------------------------------------------
if choix != "-- Tous les membres --":

    st.subheader("➕ Créer une cotisation")

    membre_sel = next(
        (m for m in membres if f"{m['nom']} {m['prenom']}" == choix),
        None
    )

    montant = st.number_input("Montant (€)", min_value=0, value=45)
    type_cot = st.selectbox("Type de cotisation", ["annuelle", "gratuite", "speciale"])

    mode_de_paiement = st.selectbox(
        "Mode de paiement",
        ["cash", "virement", "QRCode"]
    )

    paye_maintenant = st.checkbox("Le membre a payé maintenant ?", value=False)

    if paye_maintenant:
        date_paiement = st.date_input("Date de paiement", value=date.today())
    else:
        date_paiement = None

    date_expiration = st.date_input(
        "Date d'expiration",
        value=date.today().replace(year=date.today().year + 1)
    )

    remarques = st.text_area("Remarques (optionnel)", "")

    if st.button("Créer la cotisation"):

        # Vérifier cotisation active existante
        cot_active = (
            supabase.table("cotisations")
            .select("*")
            .eq("membre_id", membre_sel["id"])
            .execute()
            .data
        )

        cot_active = [
            c for c in cot_active
            if safe_date(c["date_expiration"]) and safe_date(c["date_expiration"]) > datetime.now()
        ]

        if cot_active:
            st.error("❌ Ce membre possède déjà une cotisation active.")
            st.stop()

        # Créer la cotisation
        supabase.table("cotisations").insert({
            "membre_id": membre_sel["id"],
            "montant": montant,
            "type": type_cot,
            "date_paiement": str(date_paiement) if date_paiement else None,
            "mode_de_paiement": mode_de_paiement,
            "date_expiration": str(date_expiration),
            "remarques": remarques,
            "paye": paye_maintenant,
            "statut": "active"
        }).execute()

        # Activer le membre
        supabase.table("membres").update({
            "statut": "membre",
            "actif": True
        }).eq("id", membre_sel["id"]).execute()

        st.success("🎉 Cotisation créée.")
        st.rerun()

