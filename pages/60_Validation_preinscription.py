import streamlit as st
from supabase_rest import supabase

st.set_page_config(page_title="Validation préinscription", page_icon="🐾")
st.title("🐾 Validation des préinscriptions extérieures")

# ---------------------------------------------------------
# 1. Charger les préinscriptions en attente
# ---------------------------------------------------------
preinscriptions = (
    supabase.table("preinscriptions")
    .select("*")
    .eq("statut", "En attente")
    .order("date_preinscription")
    .execute()
    .data
)

if not preinscriptions:
    st.info("Aucune préinscription en attente.")
    st.stop()

choix = st.selectbox(
    "Sélectionner une préinscription",
    options=preinscriptions,
    format_func=lambda p: f"{p['nom']} {p['prenom']} — {p['chien_nom']}"
)

# ---------------------------------------------------------
# 2. Charger la séance complète
# ---------------------------------------------------------
seance_data = (
    supabase.table("cours_seances")
    .select("*")
    .eq("id", choix["seance_id"])
    .execute()
    .data
)

if not seance_data:
    st.error(f"⚠ La séance {choix['seance_id']} n'existe pas dans cours_seances.")
    st.stop()

seance = seance_data[0]

# ---------------------------------------------------------
# 3. Charger le cours
# ---------------------------------------------------------
cours_data = (
    supabase.table("cours")
    .select("*")
    .eq("id", seance["cours_id"])
    .execute()
    .data
)

cours = cours_data[0]

# ---------------------------------------------------------
# 4. Affichage enrichi
# ---------------------------------------------------------
st.subheader("📘 Cours et séance")

st.write(f"**Cours :** {cours['nom']}")
st.write(f"**Niveau :** {cours['niveau']}")
st.write(f"**Séance ID :** {choix['seance_id']}")
st.write(f"**Date :** {seance['date_seance']}")
st.write(f"**Heure :** {seance.get('heure_debut', '—')} → {seance.get('heure_fin', '—')}")

st.subheader("👤 Personne")
st.write(f"**Nom :** {choix['nom']}")
st.write(f"**Prénom :** {choix['prenom']}")
st.write(f"**Email :** {choix['email']}")
st.write(f"**Téléphone :** {choix['telephone']}")
st.write(f"**Type :** {choix.get('type', 'exterieur')}")
st.write(f"**Source :** {choix.get('source', 'portail')}")

st.subheader("🐶 Chien")
st.write(f"**Nom :** {choix['chien_nom']}")
st.write(f"**Race :** {choix['chien_race']}")

# ---------------------------------------------------------
# 5. Validation
# ---------------------------------------------------------
if st.button(f"Valider la préinscription #{choix['id']}"):

    # -----------------------------------------------------
    # 5.1 Créer le membre non_membre
    # -----------------------------------------------------
    membre = (
        supabase.table("membres")
        .insert({
            "nom": choix["nom"],
            "prenom": choix["prenom"],
            "email": choix["email"],
            "telephone": choix["telephone"],
            "statut": "non_membre",
            "actif": False
        })
        .execute()
        .data[0]
    )

    membre_id = membre["id"]

    # -----------------------------------------------------
    # 5.2 Créer le chien
    # -----------------------------------------------------
    chien = (
        supabase.table("chiens")
        .insert({
            "nom": choix["chien_nom"],
            "race": choix["chien_race"],
            "membre_id": membre_id,
            "actif": True
        })
        .execute()
        .data[0]
    )

    chien_id = chien["id"]

    # -----------------------------------------------------
    # 5.3 Inscription réelle dans cours_inscriptions
    # -----------------------------------------------------
    supabase.table("cours_inscriptions").insert({
        "membre_id": membre_id,
        "chien_id": chien_id,
        "cours_id": cours["id"],
        "seance_id": choix["seance_id"],
        "date_seance": seance["date_seance"],
        "type": "exterieur",
        "source": "preinscription",
        "actif": True
    }).execute()

    # -----------------------------------------------------
    # 5.4 Inscription dans cours_seances_inscriptions
    # -----------------------------------------------------
    supabase.table("cours_seances_inscriptions").insert({
        "seance_id": choix["seance_id"],
        "membre_id": membre_id,
        "chien_id": chien_id,
        "actif": True
    }).execute()

    # -----------------------------------------------------
    # 5.5 Mettre à jour la préinscription
    # -----------------------------------------------------
    supabase.table("preinscriptions").update({
        "statut": "validee",
        "membre_id": membre_id,
        "chien_id": chien_id,
        "traitee": True,
        "acceptee": True,
        "type": "exterieur"
    }).eq("id", choix["id"]).execute()

    st.success("La préinscription a été validée.")
    st.info("Le membre, le chien et l'inscription au cours ont été créés.")

