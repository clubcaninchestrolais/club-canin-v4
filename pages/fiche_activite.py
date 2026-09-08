import streamlit as st
from supabase import create_client, Client
import datetime

# Sécurité : accès interne uniquement
if "user_role" not in st.session_state:
    st.error("Accès réservé au personnel du club.")
    st.stop()

if "activite_id" not in st.session_state:
    st.error("Aucune activité sélectionnée.")
    st.stop()

activite_id = st.session_state["activite_id"]

# Connexion Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# Charger l’activité
activite = (
    supabase.table("activites_speciales")
    .select("*")
    .eq("id", activite_id)
    .execute()
    .data
)

if not activite:
    st.error("Activité introuvable.")
    st.stop()

a = activite[0]

st.title(f"📝 Modifier l'activité : {a['nom']}")

# Formulaire de modification
with st.form("form_modif_activite"):
    nom = st.text_input("Nom de l'activité", a["nom"])
    date = st.date_input("Date", datetime.date.fromisoformat(a["date"]))
    prix_default = st.number_input("Prix par personne", min_value=0.0, value=float(a["prix_default"]))
    description = st.text_area("Description", a["description"] or "")
    afficher_chien = st.checkbox("Afficher le choix du chien ?", a["afficher_chien"])

    submit = st.form_submit_button("💾 Enregistrer les modifications")

    if submit:
        supabase.table("activites_speciales").update({
            "nom": nom,
            "date": date.isoformat(),
            "prix_default": prix_default,
            "description": description,
            "afficher_chien": afficher_chien
        }).eq("id", activite_id).execute()

        st.success("Activité mise à jour avec succès !")
        st.experimental_rerun()

# Liste des inscrits
st.subheader("👥 Inscriptions")

inscrits = (
    supabase.table("inscriptions_speciales")
    .select("*")
    .eq("activite_id", activite_id)
    .execute()
    .data
)

if inscrits:
    for i in inscrits:
        st.write(f"- {i['prenom']} {i['nom']} — {i['nombre']} participant(s)")
else:
    st.info("Aucun inscrit pour cette activité.")
