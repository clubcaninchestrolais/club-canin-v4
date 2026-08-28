import streamlit as st
from supabase_rest import supabase

st.set_page_config(page_title="Ajout membre", page_icon="👤")
st.title("👤 Ajouter un membre")

# ---------------------------------------------------------
# Protection anti double-clic + message persistant
# ---------------------------------------------------------
if st.session_state.get("membre_ajoute", False):
    st.success(st.session_state["membre_ajoute"])
    st.session_state["membre_ajoute"] = False
    st.stop()

# ---------------------------------------------------------
# Formulaire simple
# ---------------------------------------------------------
nom = st.text_input("Nom")
prenom = st.text_input("Prénom")
email = st.text_input("Email")
telephone = st.text_input("Téléphone")

statut = st.selectbox(
    "Statut du membre",
    ["normal", "benevole"]
)

# ---------------------------------------------------------
# Bouton d'ajout
# ---------------------------------------------------------
if st.button("Ajouter le membre"):
    if not prenom or not nom:
        st.error("Le prénom et le nom sont obligatoires.")
        st.stop()

    # Insertion du membre
    nouveau = supabase.table("membres").insert({
        "prenom": prenom,
        "nom": nom,
        "email": email,
        "telephone": telephone,
        "statut": statut
    }).execute()

    if not nouveau.data:
        st.error("Erreur lors de l'ajout du membre.")
        st.stop()

    membre_id = nouveau.data[0]["id"]

    # ---------------------------------------------------------
    # LOGIQUE AUTOMATIQUE : bénévole = gratuit
    # ---------------------------------------------------------
    if statut == "benevole":

        # Cotisation gratuite
        supabase.table("cotisations").upsert({
            "membre_id": membre_id,
            "date_expiration": "2035-01-01",
            "type": "gratuit",
            "statut": "gratuit",
            "montant": 0,
            "paye": True,
            "mode_de_paiement": "gratuit"
        }).execute()

        # Abonnement gratuit illimité
        supabase.table("abonnements").upsert({
            "membre_id": membre_id,
            "actif": True,
            "seances_total": -1,
            "seances_restantes": -1,
            "type": "gratuit"
        }).execute()

        st.session_state["membre_ajoute"] = (
            "Membre bénévole ajouté avec cotisation + abonnement gratuits !"
        )
        st.rerun()

    # ---------------------------------------------------------
    # Cas normal
    # ---------------------------------------------------------
    st.session_state["membre_ajoute"] = "Membre ajouté avec succès."
    st.rerun()
