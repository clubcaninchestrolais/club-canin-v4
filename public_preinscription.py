import streamlit as st
from supabase_rest import supabase
from datetime import date, datetime

st.set_page_config(page_title="Préinscription en ligne", page_icon="📝", layout="centered")

st.title("📝 Préinscription à un cours du Club Canin")
st.markdown("Merci de remplir ce formulaire pour préinscrire votre chien à une séance.")

# ---------------------------------------------------------
# 1. Trouver la prochaine séance disponible
# ---------------------------------------------------------
seances = (
    supabase.table("cours_seances")
    .select("*")
    .gte("date_seance", date.today().isoformat())
    .order("date_seance", desc=False)
    .limit(1)
    .execute()
    .data
)

if not seances:
    st.error("Aucune séance future disponible pour le moment.")
    st.stop()

seance = seances[0]
seance_id = seance["id"]
cours_id = seance["cours_id"]

st.info(f"Prochaine séance disponible : **{seance['date_seance']}**")

# ---------------------------------------------------------
# 2. Formulaire extérieur ou membre
# ---------------------------------------------------------
st.subheader("Vos informations")

nom = st.text_input("Nom")
prenom = st.text_input("Prénom")
email = st.text_input("Email")
telephone = st.text_input("Téléphone")

st.subheader("Informations sur votre chien")

chien_nom = st.text_input("Nom du chien")
chien_race = st.text_input("Race")
chien_naissance = st.date_input("Date de naissance", value=date(2020, 1, 1))

# ---------------------------------------------------------
# 3. Envoi du formulaire
# ---------------------------------------------------------
if st.button("Envoyer la préinscription"):

    # Vérification des champs
    if not nom or not prenom or not email or not telephone or not chien_nom or not chien_race:
        st.error("Merci de remplir tous les champs obligatoires.")
        st.stop()

    # -----------------------------------------------------
    # 4. Vérifier si l'email appartient à un membre existant
    # -----------------------------------------------------
    membres = (
        supabase.table("membres")
        .select("*")
        .eq("email", email)
        .execute()
        .data
    )

    if membres:
        # -------------------------------------------------
        # CAS 1 : C'est un membre existant
        # -------------------------------------------------
        membre = membres[0]
        membre_id = membre["id"]

        # Vérifier si le chien existe déjà
        chiens = (
            supabase.table("chiens")
            .select("*")
            .eq("membre_id", membre_id)
            .eq("nom", chien_nom)
            .execute()
            .data
        )

        if chiens:
            chien_id = chiens[0]["id"]
        else:
            # Créer le chien si pas trouvé
            chien = (
                supabase.table("chiens")
                .insert({
                    "nom": chien_nom,
                    "race": chien_race,
                    "date_naissance": chien_naissance.isoformat(),
                    "membre_id": membre_id,
                    "actif": True
                })
                .execute()
                .data[0]
            )
            chien_id = chien["id"]

        # Inscription directe à la séance
        supabase.table("cours_seances_inscriptions").insert({
            "seance_id": seance_id,
            "membre_id": membre_id,
            "chien_id": chien_id,
            "actif": True
        }).execute()

        # Préinscription validée automatiquement
        supabase.table("preinscriptions").insert({
            "nom": nom,
            "prenom": prenom,
            "email": email,
            "telephone": telephone,
            "chien_nom": chien_nom,
            "chien_race": chien_race,
            "chien_naissance": chien_naissance.isoformat(),
            "cours_id": cours_id,
            "seance_id": seance_id,
            "date_preinscription": datetime.now().isoformat(),
            "statut": "validee",
            "traitee": True,
            "acceptee": True,
            "type": "membre",
            "membre_id": membre_id,
            "chien_id": chien_id
        }).execute()

        st.success("Votre préinscription a été enregistrée et validée automatiquement.")
        st.info("Votre chien est inscrit à la prochaine séance.")
        st.stop()

    else:
        # -------------------------------------------------
        # CAS 2 : C'est un extérieur
        # -------------------------------------------------
        supabase.table("preinscriptions").insert({
            "nom": nom,
            "prenom": prenom,
            "email": email,
            "telephone": telephone,
            "chien_nom": chien_nom,
            "chien_race": chien_race,
            "chien_naissance": chien_naissance.isoformat(),
            "cours_id": cours_id,
            "seance_id": seance_id,
            "date_preinscription": datetime.now().isoformat(),
            "statut": "En attente",
            "traitee": False,
            "acceptee": None,
            "type": "exterieur",
            "membre_id": None,
            "chien_id": None
        }).execute()

        st.success("Votre préinscription a été envoyée avec succès !")
        st.info("Le club vous contactera après validation.")
