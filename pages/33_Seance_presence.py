import streamlit as st
from supabase_rest import supabase
from datetime import date

st.set_page_config(page_title="Présence séance", page_icon="📋")
st.title("📋 Validation des présences")

# ---------------------------------------------------------
# 1. Charger les séances (cours_seances)
# ---------------------------------------------------------
seances = (
    supabase.table("cours_seances")
    .select("*")
    .order("date_seance")
    .execute()
    .data
)

if not seances:
    st.info("Aucune séance disponible.")
    st.stop()

choix_seance = st.selectbox(
    "Séance",
    options=seances,
    format_func=lambda s: f"{s['date_seance']} — cours {s['cours_id']} ({s['heure_debut']})"
)

seance_id = choix_seance["id"]
cours_id = choix_seance["cours_id"]
date_seance = choix_seance["date_seance"]

st.markdown("---")

# ---------------------------------------------------------
# 2. Charger les inscrits (cours_seances_inscriptions)
# ---------------------------------------------------------
inscrits = (
    supabase.table("cours_seances_inscriptions")
    .select("*")
    .eq("seance_id", seance_id)
    .eq("actif", True)
    .execute()
    .data
)

if not inscrits:
    st.info("Aucun inscrit pour cette séance.")
    st.stop()

# ---------------------------------------------------------
# 3. Charger membres + chiens + vérifier présence existante
# ---------------------------------------------------------
liste_presence = []

for ins in inscrits:

    # Charger membre
    membre_res = (
        supabase.table("membres")
        .select("*")
        .eq("id", ins["membre_id"])
        .execute()
        .data
    )

    if not membre_res:
        st.error(f"Membre introuvable (id={ins['membre_id']}).")
        continue

    membre = membre_res[0]

    # Charger chien
    chien_res = (
        supabase.table("chiens")
        .select("*")
        .eq("id", ins["chien_id"])
        .execute()
        .data
    )

    if not chien_res:
        st.error(f"Chien introuvable (id={ins['chien_id']}).")
        continue

    chien = chien_res[0]

    # Vérifier si présence déjà enregistrée
    presence_existante = (
        supabase.table("cours_presences")
        .select("*")
        .eq("membre_id", membre["id"])
        .eq("chien_id", chien["id"])
        .eq("seance_id", seance_id)
        .execute()
        .data
    )

    if presence_existante:
        continue

    liste_presence.append({
        "inscription_id": ins["id"],
        "membre_id": membre["id"],
        "chien_id": chien["id"],
        "nom_membre": f"{membre['nom']} {membre['prenom']}",
        "nom_chien": chien["nom"]
    })

# ---------------------------------------------------------
# 4. Interface de présence
# ---------------------------------------------------------
st.subheader("Présences")

if not liste_presence:
    st.success("Toutes les présences ont déjà été validées.")
    st.stop()

presence_selection = {}
for p in liste_presence:
    presence_selection[p["inscription_id"]] = st.checkbox(
        f"{p['nom_membre']} — {p['nom_chien']}",
        key=f"presence_{p['inscription_id']}"
    )

st.markdown("---")

# ---------------------------------------------------------
# 5. Validation des présences
# ---------------------------------------------------------
if st.button("Valider les présences"):

    for p in liste_presence:
        if presence_selection[p["inscription_id"]]:

            # Enregistrer la présence dans cours_presences
            supabase.table("cours_presences").insert({
                "cours_id": cours_id,
                "seance_id": seance_id,
                "membre_id": p["membre_id"],
                "chien_id": p["chien_id"],
                "date_presence": date_seance,
                "statut": "present"
            }).execute()

            # Décrémenter l'abonnement du membre
            abo_res = (
                supabase.table("abonnements")
                .select("*")
                .eq("id_membre", p["membre_id"])
                .eq("actif", True)
                .execute()
                .data
            )

            if abo_res:
                abo = abo_res[0]

                if abo["seances_total"] != -1 and abo["seances_restantes"] > 0:
                    supabase.table("abonnements").update({
                        "seances_restantes": abo["seances_restantes"] - 1
                    }).eq("id", abo["id"]).execute()

    st.success("Présences validées.")
