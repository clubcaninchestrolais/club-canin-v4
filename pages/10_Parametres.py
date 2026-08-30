import streamlit as st
from securite import securite_admin
securite_admin()

from datetime import datetime, date
from supabase import create_client, Client
from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral


st.set_page_config(page_title="Paramètres du club", page_icon="⚙️")

hide_streamlit_menu()
menu_lateral()

st.title("⚙️ Paramètres du club")

# Charger les paramètres (une seule ligne)
params = supabase.table("parametres").select("*").execute().data[0]

# ---------------------------------------------------------
# Informations du club
# ---------------------------------------------------------
st.subheader("Informations du club")
col1, col2 = st.columns(2)

params["nom_club"] = col1.text_input("Nom du club", params["nom_club"])
params["email_club"] = col2.text_input("Email du club", params["email_club"])
params["tel_club"] = col1.text_input("Téléphone", params["tel_club"])
params["adresse_club"] = col2.text_input("Adresse", params["adresse_club"])

params["site_web_club"] = col1.text_input("Site web", params.get("site_web_club", ""))
params["iban_club"] = col2.text_input("IBAN", params.get("iban_club", ""))
params["responsable_club"] = col1.text_input("Responsable", params.get("responsable_club", ""))
params["horaire_club"] = col2.text_input("Horaire", params.get("horaire_club", ""))
params["message_accueil"] = st.text_area("Message d’accueil", params.get("message_accueil", ""))

st.markdown("---")

# ---------------------------------------------------------
# Paramètres – Paiements (NOUVEAU)
# ---------------------------------------------------------
st.subheader("💳 Paramètres – Paiements")

colP1, colP2 = st.columns(2)

params["nom_beneficiaire"] = colP1.text_input(
    "Nom du bénéficiaire (QR Paiement)",
    params.get("nom_beneficiaire", "Club Canin Chestrolais de Neufchâteau")
)

params["iban_beneficiaire"] = colP2.text_input(
    "IBAN du bénéficiaire (QR Paiement)",
    params.get("iban_beneficiaire", "BE36068954592181")
)

st.markdown("---")

# ---------------------------------------------------------
# Cotisations
# ---------------------------------------------------------
st.subheader("Cotisations")
col3, col4 = st.columns(2)

params["montant_annuel"] = col3.number_input("Montant annuel (€)", value=float(params["montant_annuel"]))
params["montant_trimestriel"] = col4.number_input("Montant trimestriel (€)", value=float(params["montant_trimestriel"]))
params["montant_mensuel"] = col3.number_input("Montant mensuel (€)", value=float(params["montant_mensuel"]))
params["frais_inscription"] = col4.number_input("Frais d'inscription (€)", value=float(params["frais_inscription"]))

params["reduction_famille"] = col3.number_input("Réduction famille (€)", value=float(params["reduction_famille"]))
params["reduction_multi_chiens"] = col4.number_input("Réduction multi‑chiens (€)", value=float(params["reduction_multi_chiens"]))

st.markdown("---")

# ---------------------------------------------------------
# Abonnements
# ---------------------------------------------------------
st.subheader("Abonnements")
col5, col6 = st.columns(2)

params["abo_12_seances_nb"] = col5.number_input(
    "Nombre séances (abonnement 12)",
    value=int(params["abo_12_seances_nb"])
)
params["abo_12_seances_prix"] = col6.number_input(
    "Prix abonnement 12 séances (€)",
    value=float(params["abo_12_seances_prix"])
)

params["abo1seance_nbre"] = col5.number_input(
    "Nombre séances (abonnement 1)",
    value=int(params["abo1seance_nbre"])
)
params["abo_1_seance_prix"] = col6.number_input(
    "Prix abonnement 1 séance (€)",
    value=float(params["abo_1_seance_prix"])
)

params["abo_benevole_prix"] = col5.number_input(
    "Prix abonnement bénévole (€)",
    value=float(params.get("abo_benevole_prix", 0))
)

params["abo_illimite_prix"] = col6.number_input(
    "Prix abonnement illimité (€)",
    value=float(params["abo_illimite_prix"]) if params["abo_illimite_prix"] else 0.0
)
params["abo_illimite_duree"] = col5.number_input(
    "Durée abonnement illimité (jours)",
    value=int(params["abo_illimite_duree"]) if params["abo_illimite_duree"] else 0
)

st.markdown("---")

# ---------------------------------------------------------
# Couleurs
# ---------------------------------------------------------
st.subheader("Couleurs (statuts)")
col7, col8 = st.columns(2)

params["couleur_expire"] = col7.text_input("Couleur expiré", params["couleur_expire"])
params["couleur_bientot"] = col8.text_input("Couleur bientôt expiré", params["couleur_bientot"])
params["couleur_jaune"] = col7.text_input("Couleur attention", params["couleur_jaune"])
params["couleur_ok"] = col8.text_input("Couleur OK", params["couleur_ok"])

st.markdown("---")

# ---------------------------------------------------------
# Sauvegarde
# ---------------------------------------------------------
if st.button("💾 Enregistrer les paramètres"):
    supabase.table("parametres").update(params).eq("id", params["id"]).execute()
    st.success("Paramètres mis à jour avec succès.")
