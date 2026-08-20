import streamlit as st
from supabase_rest import supabase
from datetime import datetime

st.set_page_config(page_title="Abonnements", page_icon="🎫")
st.title("🎫 Gestion des abonnements")

# ---------------------------------------------------------
# 1. Charger les membres
# ---------------------------------------------------------
membres = (
    supabase.table("membres")
    .select("*")
    .order("nom")
    .execute()
    .data
)

options = ["-- Tous les membres --"] + [f"{m['nom']} {m['prenom']}" for m in membres]
choix = st.selectbox("Sélectionner un membre", options)

st.markdown("---")

# ---------------------------------------------------------
# 2. Charger les abonnements
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
    abos = [a for a in abos if a["nom"] == nom_sel and a["prenom"] == prenom_sel]

# ---------------------------------------------------------
# 3. Affichage ultra-compact + bouton détail
# ---------------------------------------------------------
st.subheader("📋 Liste des abonnements")

if abos:
    for abo in abos:

        # Déterminer la couleur
        if abo["seances_total"] == -1:
            couleur = "#fff7cc"   # illimité
        elif abo["seances_restantes"] == 0:
            couleur = "#ffcccc"   # rouge
        elif abo["seances_restantes"] <= 2:
            couleur = "#ffe6cc"   # orange
        else:
            couleur = "#e6ffe6"   # vert

        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1, 2, 2, 2, 2, 1, 1, 2])

        with col1:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>"
                f"<b>{abo['id']}</b></div>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>"
                f"{abo['nom']}</div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>"
                f"{abo['prenom']}</div>",
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>"
                f"{abo['seances_total']}</div>",
                unsafe_allow_html=True
            )

        with col5:
            st.markdown(
                f"<div style='background:{couleur};padding:4px;border-radius:4px;'>"
                f"<b>{abo['seances_restantes']}</b></div>",
                unsafe_allow_html=True
            )

        with col6:
            if st.button("+1", key=f"plus_{abo['id']}"):
                supabase.table("abonnements").update({
                    "seances_restantes": abo["seances_restantes"] + 1
                }).eq("id", abo["id"]).execute()
                st.rerun()

        with col7:
            if st.button("-1", key=f"minus_{abo['id']}"):
                if abo["seances_restantes"] > 0:
                    supabase.table("abonnements").update({
                        "seances_restantes": abo["seances_restantes"] - 1
                    }).eq("id", abo["id"]).execute()
                    st.rerun()

        with col8:
            if st.button("Voir détail", key=f"detail_{abo['id']}"):
                st.session_state["abo_id"] = abo["id"]
                st.session_state["go_detail"] = True
                st.rerun()

    if st.session_state.get("go_detail", False):
        st.session_state["go_detail"] = False
        st.switch_page("pages/22_Fiche_Abonnement.py")

else:
    st.info("Aucun abonnement trouvé.")

st.markdown("---")

# ---------------------------------------------------------
# 4. Création d’un abonnement manuel (avec contrôle cotisation)
# ---------------------------------------------------------
if choix != "-- Tous les membres --":
    st.subheader("➕ Créer un abonnement")

    types_abonnements = {
        "Abonnement 12 séances": 12,
        "Abonnement 20 séances": 20,
        "Abonnement illimité": -1
    }

    type_abo = st.selectbox("Type d’abonnement", list(types_abonnements.keys()))
    total = types_abonnements[type_abo]

    membre_sel = next((m for m in membres if f"{m['nom']} {m['prenom']}" == choix), None)

    if st.button("Créer l’abonnement"):

        # ---------------------------------------------------------
        # 🔒 Vérification cotisation active
        # ---------------------------------------------------------
        cotisation = (
            supabase.table("cotisations")
            .select("*")
            .eq("membre_id", membre_sel["id"])
            .eq("actif", True)
            .execute()
            .data
        )

        if not cotisation:
            st.error("❌ Impossible de créer un abonnement : ce membre n'a pas de cotisation active.")
            st.stop()

        # ---------------------------------------------------------
        # ✔ Création de l’abonnement
        # ---------------------------------------------------------
        supabase.table("abonnements").insert({
            "membre_id": membre_sel["id"],
            "seances_total": total,
            "seances_restantes": total,
            "date_achat": datetime.now().date().isoformat(),
            "actif": True
        }).execute()

        st.success("🎉 Abonnement créé avec succès.")
        st.rerun()

else:
    st.info("Sélectionnez un membre pour créer un abonnement.")
