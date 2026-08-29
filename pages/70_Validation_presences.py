import streamlit as st
from supabase import create_client, Client
import datetime

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Validation des présences")

aujourdhui = datetime.date.today().isoformat()

# Charger les séances du jour
seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("date_seance", aujourdhui)
    .order("cours_id")
    .execute()
    .data
)

if not seances:
    st.info("Aucune séance aujourd'hui.")
    st.stop()

# Charger les cours
cours_raw = supabase.table("cours").select("*").execute().data
cours_dict = {c["id"]: c for c in cours_raw}

# Construire la liste des participants (MEMBRES UNIQUEMENT)
participants = []

for seance in seances:
    seance_id = seance["id"]
    cours_id = seance["cours_id"]

    # Membres inscrits à ce cours
    inscriptions = (
        supabase.table("cours_inscriptions")
        .select("*")
        .eq("cours_id", cours_id)
        .execute()
        .data
    )

    for ins in inscriptions:
        membre = supabase.table("membres").select("*").eq("id", ins["membre_id"]).execute().data
        chien = supabase.table("chiens").select("*").eq("id", ins["chien_id"]).execute().data

        if membre and chien:
            participants.append({
                "membre": membre[0],
                "chien": chien[0],
                "cours_id": cours_id,
                "cours_nom": cours_dict[cours_id]["nom_cours"],
                "seance_id": seance_id,
                "seance_nom": seance["nom_seance"],
                "inscription_id": ins["id"]
            })

# -----------------------------
# 🔍 FILTRES EN HAUT DE PAGE
# -----------------------------

# Filtre par cours
liste_cours = ["Tous"] + sorted({p["cours_nom"] for p in participants})
filtre_cours = st.selectbox("Filtrer par cours :", liste_cours)

# Filtre par nom
filtre_nom = st.text_input("Filtrer par nom :").strip().lower()

# -----------------------------
# 🔍 APPLICATION DES FILTRES
# -----------------------------

filtered = participants

if filtre_cours != "Tous":
    filtered = [p for p in filtered if p["cours_nom"] == filtre_cours]

if filtre_nom:
    filtered = [
        p for p in filtered
        if filtre_nom in p["membre"]["nom"].lower()
        or filtre_nom in p["membre"]["prenom"].lower()
        or filtre_nom in p["chien"]["nom"].lower()
    ]

# Tri alphabétique
filtered = sorted(filtered, key=lambda p: (p["membre"]["nom"], p["membre"]["prenom"], p["chien"]["nom"]))

# -----------------------------
# 📋 AFFICHAGE + VALIDATION
# -----------------------------

if not filtered:
    st.warning("Aucun membre ne correspond aux filtres.")
    st.stop()

for p in filtered:

    membre = p["membre"]
    chien = p["chien"]
    cours_nom = p["cours_nom"]
    seance_nom = p["seance_nom"]
    seance_id = p["seance_id"]

    # Vérifier présence
    presence = (
        supabase.table("cours_presences")
        .select("*")
        .eq("membre_id", membre["id"])
        .eq("chien_id", chien["id"])
        .eq("seance_id", seance_id)
        .execute()
        .data
    )

    deja = bool(presence)

    st.markdown(
        f"""
        <div style='background:#f7f7f7;padding:12px;border-radius:8px;margin-bottom:10px;'>
            <b>{membre['prenom']} {membre['nom']}</b><br>
            🐶 {chien['nom']}<br>
            📘 {cours_nom}<br>
            🕒 {seance_nom}
        </div>
        """,
        unsafe_allow_html=True
    )

    if not deja:
        if st.button(
            f"Valider présence de {membre['prenom']} {membre['nom']}",
            key=f"btn_{p['inscription_id']}"
        ):
            supabase.table("cours_presences").insert({
                "membre_id": membre["id"],
                "chien_id": chien["id"],
                "seance_id": seance_id,
                "present": True
            }).execute()

            # Décrémenter abonnement
            abo = (
                supabase.table("abonnements")
                .select("*")
                .eq("id_membre", membre["id"])
                .order("id", desc=True)
                .execute()
                .data
            )

            if abo:
                rest = abo[0]["seances_restantes"]
                if rest > 0:
                    supabase.table("abonnements").update({
                        "seances_restantes": rest - 1
                    }).eq("id", abo[0]["id"]).execute()

            st.success("Présence validée.")
            st.rerun()

    else:
        st.success("Présence déjà validée.")
