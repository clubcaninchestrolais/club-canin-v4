import streamlit as st
from supabase_rest import supabase
from datetime import datetime, date

st.set_page_config(page_title="Abonnements", page_icon="🎫")
st.title("🎫 Gestion des abonnements")

# ---------------------------------------------------------
# Fonction date sécurisée
# ---------------------------------------------------------
def safe_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", ""))
    except:
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
# Charger les abonnements
# ---------------------------------------------------------
abos = (
    supabase.table("abonnements")
    .select("*")
    .order("id", desc=True)
    .execute()
    .data
)

# Ajouter nom + prénom
for abo in abos:
    membre = next((m for m in membres if m["id"] == abo["membre_id"]), None)
    if membre:
        abo["nom"] = membre["nom"]
        abo["prenom"] = membre["prenom"]

# Filtrer si un membre est sélectionné
if choix != "-- Tous les membres --":
    nom_sel, prenom_sel = choix.split(" ")
    abos = [
        a for a in abos
        if a["nom"] == nom_sel and a["prenom"] == prenom_sel
    ]

# ---------------------------------------------------------
# Affichage ultra-compact LARGE (version parfaite)
# ---------------------------------------------------------
st.subheader("📋 Liste des abonnements")

if abos:
    for abo in abos:

        date_pay = safe_date(abo.get("date_paiement"))
        date_exp = safe_date(abo.get("date_expiration"))

        # Déterminer la couleur
        if abo.get("paye"):
            couleur = "#e6ffe6"  # vert
        else:
            if date_exp:
                jours = (date_exp - datetime.now()).days
                if jours < 0:
                    couleur = "#ffcccc"  # rouge
                elif jours <= 30:
                    couleur = "#ffe6cc"  # orange
                else:
                    couleur = "#ffcccc"
            else:
                couleur = "#ffcccc"

        # 6 colonnes larges comme dans cotisation
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])

        with col1:
            st.markdown(
                f"<div style='background:{couleur};padding:6px;border-radius:4px;'>"
                f"<b>{abo['id']}</b></div>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div style='background:{couleur};padding:6px;border-radius:4px;'>"
                f"{abo['nom']}</div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div style='background:{couleur};padding:6px;border-radius:4px;'>"
                f"{abo['prenom']}</div>",
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"<div style='background:{couleur};padding:6px;border-radius:4px;'>"
                f"{abo['seances_total']}</div>",
                unsafe_allow_html=True
            )

        with col5:
            st.markdown(
                f"<div style='background:{couleur};padding:6px;border-radius:4px;'>"
                f"<b>{abo['seances_restantes']}</b></div>",
                unsafe_allow_html=True
            )

        # Colonne des boutons regroupés proprement
        with col6:
            b1, b2, b3 = st.columns([1, 1, 2])

            with b1:
                if st.button("+1", key=f"plus_{abo['id']}"):
                    supabase.table("abonnements").update({
                        "seances_restantes": abo["seances_restantes"] + 1
                    }).eq("id", abo["id"]).execute()
                    st.rerun()

            with b2:
                if st.button("-1", key=f"minus_{abo['id']}"):
                    if abo["seances_restantes"] > 0:
                        supabase.table("abonnements").update({
                            "seances_restantes": abo["seances_restantes"] - 1
                        }).eq("id", abo["id"]).execute()
                        st.rerun()

            with b3:
                if st.button("Voir détail", key=f"detail_{abo['id']}"):
                    st.session_state["abo_id"] = abo["id"]
                    st.session_state["go_detail"] = True
                    st.rerun()

    # Navigation stable
    if st.session_state.get("go_detail", False):
        st.session_state["go_detail"] = False
        st.switch_page("Fiche Abonnement")

else:
    st.info("Aucun abonnement trouvé.")

st.markdown("---")

# ---------------------------------------------------------
# Création d’un abonnement
# ---------------------------------------------------------
if choix != "-- Tous les membres --":

    st.subheader("➕ Créer un abonnement")

    membre_sel = next(
        (m for m in membres if f"{m['nom']} {m['prenom']}" == choix),
        None
    )

    types_abonnements = {
        "Abonnement 12 séances": 12,
        "Abonnement 20 séances": 20,
        "Abonnement illimité": -1
    }

    type_abo = st.selectbox("Type d’abonnement", list(types_abonnements.keys()))
    total = types_abonnements[type_abo]

    if st.button("Créer l’abonnement"):

        cotisations = (
            supabase.table("cotisations")
            .select("*")
            .eq("membre_id", membre_sel["id"])
            .execute()
            .data
        )

        cot_active = [
            c for c in cotisations
            if c["date_expiration"] and datetime.fromisoformat(c["date_expiration"]) > datetime.now()
        ]

        if not cot_active:
            st.error("❌ Impossible : ce membre n'a pas de cotisation active.")
            st.stop()

        supabase.table("abonnements").insert({
            "membre_id": membre_sel["id"],
            "seances_total": total,
            "seances_restantes": total,
            "date_achat": datetime.now().date().isoformat(),
            "actif": True,
            "paye": False,
            "date_paiement": None,
            "date_expiration": None
        }).execute()

        st.success("🎉 Abonnement créé avec succès.")
        st.rerun()

else:
    st.info("Sélectionnez un membre pour créer un abonnement.")


