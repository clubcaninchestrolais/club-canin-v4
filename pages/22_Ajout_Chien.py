import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

import datetime
from supabase import create_client
from supabase_rest import log_action   # ← AUDIT

st.set_page_config(page_title="Ajouter un chien", page_icon="🐶", layout="wide")

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("🐶 Ajouter un chien")

# ---------------------------------------------------------
# Protection anti double-clic + message persistant
# ---------------------------------------------------------
if st.session_state.get("chien_ajoute", False):
    st.success(st.session_state["chien_ajoute"])
    st.session_state["chien_ajoute"] = False
    st.stop()

# ---------------------------------------------------------
# Charger les membres pour choisir le propriétaire
# ---------------------------------------------------------
membres = (
    supabase.table("membres")
    .select("id, nom, prenom")
    .eq("archive", False)
    .execute()
    .data
)

membres = sorted(membres, key=lambda m: (m["nom"].lower(), m["prenom"].lower()))
liste_affichage = [f"{m['nom']} {m['prenom']}" for m in membres]
proprietaire_nom = st.selectbox("Propriétaire du chien", liste_affichage)
id_membre = next(m["id"] for m in membres if f"{m['nom']} {m['prenom']}" == proprietaire_nom)

# ---------------------------------------------------------
# Validation numéro de puce (15 chiffres)
# ---------------------------------------------------------
def valide_puce(puce):
    if not puce:
        return False
    puce_clean = puce.replace(" ", "")
    return puce_clean.isdigit() and len(puce_clean) == 15

# ---------------------------------------------------------
# Formulaire complet
# ---------------------------------------------------------
with st.form("form_chien"):

    st.subheader("Informations générales")
    nom = st.text_input("Nom du chien")
    race = st.text_input("Race")
    sexe = st.selectbox("Sexe", ["Mâle", "Femelle", "Inconnu"])
    date_naissance = st.date_input("Date de naissance", format="DD/MM/YYYY")

    st.subheader("Identification")
    numero_puce = st.text_input("Numéro de puce (15 chiffres)")
    identification = st.text_input("Identification")

    st.subheader("Santé")
    vaccins = st.text_input("Vaccins")
    date_vaccin = st.date_input("Date du dernier vaccin", format="DD/MM/YYYY")

    st.subheader("Activité & remarques")
    activite = st.selectbox("Activité", ["OBE", "AGI", "OBE/AGI"])
    remarques = st.text_area("Remarques")

    st.subheader("Photo")
    photo_url = st.text_input("URL de la photo")

    submit = st.form_submit_button("Ajouter le chien")

# ---------------------------------------------------------
# TRAITEMENT APRÈS LE FORMULAIRE
# ---------------------------------------------------------
if submit:

    # Vérification numéro de puce
    if not valide_puce(numero_puce):
        st.error("❌ Le numéro de puce doit contenir exactement 15 chiffres.")
        st.stop()

    # Insertion du chien
    supabase.table("chiens").insert({
        "nom": nom,
        "race": race,
        "sexe": sexe,
        "date_naissance": date_naissance.isoformat(),
        "numero_puce": numero_puce.replace(" ", ""),
        "identification": identification,
        "vaccins": vaccins,
        "date_vaccin": date_vaccin.isoformat(),
        "activite": activite,
        "remarques": remarques,
        "photo_url": photo_url,
        "id_membre": id_membre,
        "archive": False
    }).execute()

    # AUDIT
    log_action("Ajout chien", f"{nom} — utilisateur : {st.session_state.get('username', 'inconnu')}")


    # Message persistant
    st.session_state["chien_ajoute"] = "🐶 Chien ajouté avec succès !"

    # RERUN (autorisé car hors du formulaire)
    st.rerun()
