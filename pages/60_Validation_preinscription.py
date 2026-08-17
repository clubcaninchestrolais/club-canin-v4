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

st.subheader("Détails")
st.write(f"**Nom :** {choix['nom']}")
st.write(f"**Prénom :** {choix['prenom']}")
st.write(f"**Email :** {choix['email']}")
st.write(f"**Téléphone :** {choix['telephone']}")
st.write(f"**Chien :** {choix['chien_nom']} ({choix['chien_race']})")

# ---------------------------------------------------------
# 2. Validation
# ---------------------------------------------------------
if st.button("Valider la préinscription"):

    # -----------------------------------------------------
    # 2.1 Créer le membre non_membre
    # -----------------------------------------------------
    membre = (
        supabase.table("membres")
        .insert({
            "nom": choix["nom"],
            "prenom": choix["prenom"],
            "email": choix["email"],
            "telephone": choix["telephone"],
            "statut": "non_membre",
            "actif": False          # ❗ CORRECTION IMPORTANTE
        })
        .execute()
        .data[0]
    )

    membre_id = membre["id"]

    # -----------------------------------------------------
    # 2.2 Créer le chien (sans liaison)
    # -----------------------------------------------------
    chien = (
        supabase.table("chiens")
        .insert({
            "nom": choix["chien_nom"],
            "race": choix["chien_race"],
            "membre_id": None,      # ❗ CORRECTION IMPORTANTE
            "actif": True
        })
        .execute()
        .data[0]
    )

    chien_id = chien["id"]

    # -----------------------------------------------------
    # 2.3 Inscrire à la séance
    # -----------------------------------------------------
    supabase.table("cours_seances_inscriptions").insert({
        "seance_id": choix["seance_id"],
        "membre_id": membre_id,
        "chien_id": chien_id,
        "actif": True
    }).execute()

    # -----------------------------------------------------
    # 2.4 Mettre à jour la préinscription
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
    st.info("Le membre non_membre et le chien ont été créés.")
