import streamlit as st
from securite import securite_user
securite_user()

from datetime import datetime, date
from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

st.set_page_config(page_title="Abonnements", page_icon="🎫", layout="wide")
hide_streamlit_menu()
menu_lateral()

st.title("🎫 Gestion des abonnements")

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
# Filtre Actifs / Terminés / Tous
# ---------------------------------------------------------
filtre = st.radio(
    "Afficher",
    ["Tous les abonnements", "Actifs uniquement", "Terminés uniquement"],
    horizontal=True
)

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
        abo["statut_membre"] = membre["statut"]

# Filtrer si un membre est sélectionné
if choix != "-- Tous les membres --":
    nom_sel, prenom_sel = choix.split(" ")
    abos = [
        a for a in abos
        if a["nom"] == nom_sel and a["prenom"] == prenom_sel
    ]

# ---------------------------------------------------------
# Appliquer le filtre
# ---------------------------------------------------------
if filtre == "Actifs uniquement":
    abos = [a for a in abos if a["seances_restantes"] != 0]

elif filtre == "Terminés uniquement":
    abos = [a for a in abos if a["seances_restantes"] == 0]

# ---------------------------------------------------------
# Affichage ultra-compact
# ---------------------------------------------------------
st.subheader("📋 Liste des abonnements")

if "abo_id" not in st.session_state:
    st.session_state["abo_id"] = None

if abos:
    # ⭐⭐ AJOUTER LES ENTÊTES ICI ⭐⭐
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])

    with col1:
        st.markdown("**ID**")
    with col2:
        st.markdown("**Nom**")
    with col3:
        st.markdown("**Prénom**")
    with col4:
        st.markdown("**Total**")
    with col5:
        st.markdown("**Restant**")
    with col6:
        st.markdown("**Actions**")
    for abo in abos:

        rest = abo["seances_restantes"]

        # Déterminer la couleur
        if abo["statut"] == "gratuit":
            couleur = "#cce6ff"  # bleu bénévole
        elif rest == 0:
            couleur = "#ffcccc"  # rouge = terminé
        elif rest <= 2:
            couleur = "#ffe6cc"  # orange = alerte
        else:
            couleur = "#e6ffe6"  # vert = OK

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
            if abo["statut"] == "gratuit":
                st.markdown(
                    f"<div style='background:{couleur};padding:6px;border-radius:4px;'>"
                    f"Illimité</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background:{couleur};padding:6px;border-radius:4px;'>"
                    f"{abo['seances_total']}</div>",
                    unsafe_allow_html=True
                )

        with col5:
            if abo["statut"] == "gratuit":
                st.markdown(
                    f"<div style='background:{couleur};padding:6px;border-radius:4px;'>"
                    f"∞</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background:{couleur};padding:6px;border-radius:4px;'>"
                    f"<b>{abo['seances_restantes']}</b></div>",
                    unsafe_allow_html=True
                )

        with col6:
            b1, b2, b3 = st.columns([1, 1, 2])

            # Pas de +1 / -1 pour les bénévoles
            if abo["statut"] != "gratuit":

                with b1:
                    if st.button("+1", key=f"plus_{abo['id']}"):
                        supabase.table("abonnements").update({
                            "seances_restantes": abo["seances_restantes"] + 1,
                            "statut": "actif"
                        }).eq("id", abo["id"]).execute()
                        st.rerun()

                with b2:
                    if st.button("-1", key=f"minus_{abo['id']}"):
                        new_count = max(abo["seances_restantes"] - 1, 0)
                        statut = "actif" if new_count > 0 else "termine"

                        supabase.table("abonnements").update({
                            "seances_restantes": new_count,
                            "statut": statut
                        }).eq("id", abo["id"]).execute()
                        st.rerun()

            with b3:
                if st.button("Voir détail", key=f"detail_{abo['id']}"):
                    st.session_state["abo_id"] = abo["id"]
                    st.rerun()

else:
    st.info("Aucun abonnement trouvé.")

st.markdown("---")

# ---------------------------------------------------------
# FICHE ABONNEMENT
# ---------------------------------------------------------
if st.session_state["abo_id"] is not None:
    abo_id = st.session_state["abo_id"]

    abo = (
        supabase.table("abonnements")
        .select("*")
        .eq("id", abo_id)
        .execute()
        .data
    )

    if abo:
        abo = abo[0]

        membre = (
            supabase.table("membres")
            .select("*")
            .eq("id", abo["membre_id"])
            .execute()
            .data[0]
        )

        st.subheader("📄 Détail de l'abonnement")

        st.markdown("### 👤 Informations du membre")
        st.write(f"**Nom :** {membre['nom']}")
        st.write(f"**Prénom :** {membre['prenom']}")
        st.write(f"**Statut membre :** {membre['statut']}")

        st.markdown("---")

        st.markdown("### 🎫 Informations de l'abonnement")

        if abo["statut"] == "gratuit":
            st.write("**Type :** Abonnement gratuit bénévole")
            st.write("**Séances :** Illimitées")
            st.write("**Prix :** 0 €")
        else:
            st.write(f"**Total séances :** {abo['seances_total']}")
            st.write(f"**Séances restantes :** {abo['seances_restantes']}")
            st.write(f"**Prix :** {abo.get('prix', 'N/A')} €")

        st.write(f"**Date d'achat :** {abo['date_achat']}")
        st.write(f"**Statut :** {abo['statut']}")

        st.markdown("---")

        # Pas de modification pour les bénévoles
        if abo["statut"] != "gratuit":

            col1, col2 = st.columns(2)

            with col1:
                if st.button("➕ Ajouter une séance", key="fiche_plus"):
                    supabase.table("abonnements").update({
                        "seances_restantes": abo["seances_restantes"] + 1,
                        "statut": "actif"
                    }).eq("id", abo_id).execute()
                    st.success("Séance ajoutée.")
                    st.rerun()

            with col2:
                if st.button("➖ Retirer une séance", key="fiche_minus"):
                    new_count = max(abo["seances_restantes"] - 1, 0)
                    statut = "actif" if new_count > 0 else "termine"

                    supabase.table("abonnements").update({
                        "seances_restantes": new_count,
                        "statut": statut
                    }).eq("id", abo_id).execute()

                    st.success("Séance retirée.")
                    st.rerun()

        st.markdown("---")

        if st.button("⬅️ Fermer la fiche"):
            st.session_state["abo_id"] = None
            st.rerun()
# ---------------------------------------------------------
# SECTION CRÉATION ABONNEMENT (VERSION SÉCURISÉE)
# ---------------------------------------------------------
st.markdown("---")
st.subheader("➕ Créer un abonnement")

if choix == "-- Tous les membres --":
    st.info("Sélectionnez un membre pour créer un abonnement.")
else:
    membre_sel = next(
        (m for m in membres if f"{m['nom']} {m['prenom']}" == choix),
        None
    )

    # ---------------------------------------------------------
    # Types d'abonnements corrigés + gratuit bénévole
    # ---------------------------------------------------------
    types_abonnements = {
        "Abonnement 12 séances (30 €)": {"seances": 12, "prix": 30, "statut": "actif"},
        "Abonnement 1 séance (3 €)": {"seances": 1, "prix": 3, "statut": "actif"},
        "Abonnement gratuit bénévole": {"seances": -1, "prix": 0, "statut": "gratuit"}
    }

    # Si le membre n'est pas bénévole → on masque l'abonnement gratuit
    if membre_sel["statut"] != "benevole":
        del types_abonnements["Abonnement gratuit bénévole"]

    type_abo = st.selectbox("Type d’abonnement", list(types_abonnements.keys()))

    total = types_abonnements[type_abo]["seances"]
    prix = types_abonnements[type_abo]["prix"]
    statut_final = types_abonnements[type_abo]["statut"]

    if st.button("Créer l’abonnement"):

        # ---------------------------------------------------------
        # Vérifier cotisation active payée (sauf bénévoles)
        # ---------------------------------------------------------
        if membre_sel["statut"] != "benevole":

            cotisations = (
                supabase.table("cotisations")
                .select("*")
                .eq("membre_id", membre_sel["id"])
                .execute()
                .data
            )

            cot_active = [
                c for c in cotisations
                if c["statut"] == "active" and c["paye"] == True
            ]

            if not cot_active:
                st.error("❌ Impossible : ce membre n'a pas de cotisation active payée.")
                st.stop()

        # ---------------------------------------------------------
        # Désactiver les anciens abonnements du membre
        # ---------------------------------------------------------
        supabase.table("abonnements").update({
            "actif": False,
            "statut": "termine"
        }).eq("membre_id", membre_sel["id"]).execute()

        # ---------------------------------------------------------
        # Créer le nouvel abonnement (ACTIF = TRUE GARANTI)
        # ---------------------------------------------------------
        supabase.table("abonnements").insert({
            "membre_id": membre_sel["id"],
            "seances_total": total,
            "seances_restantes": total,
            "date_achat": datetime.now().date().isoformat(),
            "statut": statut_final,
            "prix": prix,
            "actif": True if statut_final != "termine" else False
        }).execute()

        st.success("🎉 Abonnement créé avec succès.")
        st.rerun()


