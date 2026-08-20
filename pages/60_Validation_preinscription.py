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

# ---------------------------------------------------------
# 2. Filtre
# ---------------------------------------------------------
filtre = st.text_input("🔍 Rechercher (nom, prénom, chien)")

if filtre:
    f = filtre.lower()
    preinscriptions = [
        p for p in preinscriptions
        if f in p["nom"].lower()
        or f in p["prenom"].lower()
        or f in p["chien_nom"].lower()
    ]

# ---------------------------------------------------------
# 3. Affichage en liste
# ---------------------------------------------------------
st.subheader("📋 Préinscriptions en attente")

for p in preinscriptions:

    # Charger la séance
    seance_data = (
        supabase.table("cours_seances")
        .select("*")
        .eq("id", p["seance_id"])
        .execute()
        .data
    )

    if not seance_data:
        continue

    seance = seance_data[0]

    # Charger le cours
    cours_data = (
        supabase.table("cours")
        .select("*")
        .eq("id", seance["cours_id"])
        .execute()
        .data
    )

    cours = cours_data[0]

    # Ligne compacte
    col1, col2, col3 = st.columns([4, 3, 2])

    with col1:
        st.write(f"**{p['nom']} {p['prenom']}** — {p['chien_nom']}")

    with col2:
        st.write(f"{cours['nom']} — {seance['date_seance']}")

    with col3:
        if st.button("Valider", key=f"valider_{p['id']}"):

            # Créer le membre
            membre = (
                supabase.table("membres")
                .insert({
                    "nom": p["nom"],
                    "prenom": p["prenom"],
                    "email": p["email"],
                    "telephone": p["telephone"],
                    "statut": "non_membre",
                    "actif": False
                })
                .execute()
                .data[0]
            )

            membre_id = membre["id"]

            # Créer le chien
            chien = (
                supabase.table("chiens")
                .insert({
                    "nom": p["chien_nom"],
                    "race": p["chien_race"],
                    "membre_id": membre_id,
                    "actif": True
                })
                .execute()
                .data[0]
            )

            chien_id = chien["id"]

            # Inscription réelle
            supabase.table("cours_inscriptions").insert({
                "membre_id": membre_id,
                "chien_id": chien_id,
                "cours_id": cours["id"],
                "seance_id": p["seance_id"],
                "date_seance": seance["date_seance"],
                "type": "exterieur",
                "source": "preinscription",
                "actif": True
            }).execute()

            # Inscription séance
            supabase.table("cours_seances_inscriptions").insert({
                "seance_id": p["seance_id"],
                "membre_id": membre_id,
                "chien_id": chien_id,
                "actif": True
            }).execute()

            # Mise à jour préinscription
            supabase.table("preinscriptions").update({
                "statut": "validee",
                "membre_id": membre_id,
                "chien_id": chien_id,
                "traitee": True,
                "acceptee": True,
                "type": "exterieur"
            }).eq("id", p["id"]).execute()

            st.success(f"Préinscription #{p['id']} validée.")
            st.experimental_rerun()



