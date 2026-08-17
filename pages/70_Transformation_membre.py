import streamlit as st
from supabase_rest import supabase
from datetime import datetime, timedelta

st.set_page_config(page_title="Transformation membre", page_icon="🐾")
st.title("🐾 Transformation d'un non_membre en membre")

# ---------------------------------------------------------
# 1. Charger les non_membres
# ---------------------------------------------------------
non_membres = (
    supabase.table("membres")
    .select("*")
    .eq("statut", "non_membre")
    .order("nom")
    .execute()
    .data
)

if not non_membres:
    st.info("Aucun non_membre à transformer.")
    st.stop()

options = [f"{m['nom']} {m['prenom']}" for m in non_membres]
choix = st.selectbox("Sélectionner un non_membre", options)

membre_sel = next((m for m in non_membres if f"{m['nom']} {m['prenom']}" == choix), None)
membre_id = membre_sel["id"]

st.markdown("---")

# ---------------------------------------------------------
# 2. Charger les paramètres réels
# ---------------------------------------------------------
params_all = supabase.table("parametres").select("*").execute().data

params = next((p for p in params_all if "montant_defaut" in p and p["montant_defaut"] is not None), None)

if not params:
    st.error("Impossible de trouver 'montant_defaut' dans la table parametres.")
    st.stop()

cotisation_montant = params["montant_defaut"]
cotisation_duree = params["duree_cotisation"]
prix_12 = params["abonnement_12_lecons"]
prix_1 = params["abonnement_1_lecon"]

# ---------------------------------------------------------
# 3. Choix du type d’abonnement
# ---------------------------------------------------------
st.subheader("Choix de l'abonnement")

type_abonnement = st.selectbox(
    "Sélectionner le type d'abonnement",
    ["Abonnement 12 séances (30 €)", "Abonnement 1 séance (3 €)"]
)

if type_abonnement.startswith("Abonnement 12"):
    nb_seances = 12
    prix_abonnement = prix_12
else:
    nb_seances = 1
    prix_abonnement = prix_1

st.markdown("---")

# ---------------------------------------------------------
# 4. Bouton de transformation
# ---------------------------------------------------------
if st.button("Transformer en membre"):

    # 4.1 Mise à jour du statut
    supabase.table("membres").update({
        "statut": "membre",
        "actif": True
    }).eq("id", membre_id).execute()

    # 4.2 Création de la cotisation annuelle
    supabase.table("cotisations").insert({
        "membre_id": membre_id,
        "montant": cotisation_montant,
        "date_paiement": datetime.now().date().isoformat(),
        "date_expiration": (datetime.now() + timedelta(days=cotisation_duree)).date().isoformat(),
        "type": "annuelle"
    }).execute()

    # 4.3 Création de l'abonnement (séances)
    supabase.table("abonnements").insert({
        "membre_id": membre_id,
        "seances_total": nb_seances,
        "seances_restantes": nb_seances,
        "prix": prix_abonnement,
        "date_achat": datetime.now().date().isoformat(),
        "actif": True
    }).execute()

    # ---------------------------------------------------------
    # 4.4 LIAISON CHIEN → MEMBRE via preinscriptions
    # ---------------------------------------------------------
    pre = (
        supabase.table("preinscriptions")
        .select("chien_id")
        .eq("membre_id", membre_id)
        .eq("statut", "validee")
        .execute()
        .data
    )

    if pre and pre[0]["chien_id"]:
        chien_id = pre[0]["chien_id"]

        supabase.table("chiens").update({
            "membre_id": membre_id
        }).eq("id", chien_id).execute()

    st.success("Transformation effectuée avec succès.")
    st.rerun()
