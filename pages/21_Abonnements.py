import streamlit as st
from supabase_rest import supabase
from datetime import datetime

st.set_page_config(page_title="Abonnements", page_icon="🎫")
st.title("🎫 Gestion des abonnements")

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

# Filtrer
if choix != "-- Tous les membres --":
    nom_sel, prenom_sel = choix.split(" ")
    abos = [a for a in abos if a["nom"] == nom_sel and a["prenom"] == prenom_sel]

# ---------------------------------------------------------
# Affichage
# ---------------------------------------------------------
st.subheader("📋 Liste des abonnements")

if abos:
    for abo in abos:

        # Couleur
        couleur = "#e6ffe6" if abo.get("paye") else "#ffcccc"

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
                    st.switch_page("Fiche Abonnement")

else:
    st.info("Aucun abonnement trouvé.")


