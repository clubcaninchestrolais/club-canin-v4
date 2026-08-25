import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

import datetime
from supabase import create_client

st.set_page_config(page_title="Ajouter un chien", page_icon="🐶", layout="wide")

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("🐶 Ajouter un chien")

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

# Tri alphabétique NOM + PRÉNOM
membres = sorted(membres, key=lambda m: (m["nom"].lower(), m["prenom"].lower()))

# Liste triée pour affichage
liste_affichage = [f"{m['nom']} {m['prenom']}" for m in membres]

# Sélecteur alphabétique
proprietaire_nom = st.selectbox("Propriétaire du chien", liste_affichage)

# Retrouver l'id du membre choisi
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

    # Date JJ/MM/AAAA
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

    if submit:

        # Vérification numéro de puce
        if not valide_puce(numero_puce):
            st.error("❌ Le numéro de puce doit contenir exactement 15 chiffres.")
            st.stop()

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

        st.success("🐶 Chien ajouté avec succès !")

        # Retour à la fiche du propriétaire
        st.session_state["membre_id"] = id_membre
        st.switch_page("pages/21_Fiche_Membre.py")
