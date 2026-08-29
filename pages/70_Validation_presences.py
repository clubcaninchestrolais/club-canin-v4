import streamlit as st
from supabase import create_client, Client
import datetime

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Validation des présences")

aujourdhui = datetime.date.today().isoformat()

# Charger toutes les séances
seances_raw = (
    supabase.table("cours_seances")
    .select("*")
    .order("id")
    .execute()
    .data
)

seances = [
    s for s in seances_raw
    if s["date_seance"][:10] == aujourdhui
]

if not seances:
    st.info("Aucune séance aujourd'hui.")
    st.stop()

for seance in seances:

    seance_id = int(seance["id"])   # ← CORRECTION

    st.markdown(f"### 🐾 {seance['nom_seance']} — {seance['date_seance'][:10]}")

    # EXTÉRIEURS
    exterieurs = (
        supabase.table("preinscriptions")
        .select("*")
        .eq("seance_id", seance_id)
        .eq("acceptee", True)
        .execute()
        .data
    )

    # INSCRIPTIONS
    inscriptions_raw = (
        supabase.table("cours_inscriptions")
        .select("*")
        .execute()
        .data
    )

    inscriptions = [
        ins for ins in inscriptions_raw
        if int(ins["seance_id"]) == seance_id   # ← CORRECTION
    ]

    membres_inscrits = []
    for ins in inscriptions:

        try:
            membre_id = int(ins["membre_id"])
            chien_id = int(ins["chien_id"])
            seance_id_ins = int(ins["seance_id"])   # ← CORRECTION
        except:
            continue

        membre = (
            supabase.table("membres")
            .select("*")
            .eq("id", membre_id)
            .execute()
            .data
        )
        chien = (
            supabase.table("chiens")
            .select("*")
            .eq("id", chien_id)
            .execute()
            .data
        )

        if not membre or not chien:
            continue

        membres_inscrits.append({
            "inscription_id": ins["id"],
            "membre": membre[0],
            "chien": chien[0],
            "seance_id": seance_id_ins   # ← CORRECTION
        })

    # AFFICHAGE MEMBRES
    for item in membres_inscrits:
        membre = item["membre"]
        chien = item["chien"]
        seance_id = int(item["seance_id"])   # ← CORRECTION

        presence = (
            supabase.table("cours_presences")
            .select("*")
            .eq("membre_id", membre["id"])
            .eq("chien_id", chien["id"])
            .eq("seance_id", seance_id)   # ← CORRECTION
            .execute()
            .data
        )

        deja = bool(presence)

        if not deja:
            if st.button(
                f"Valider présence {item['inscription_id']}",
                key=f"btn_membre_{item['inscription_id']}"
            ):
                insertion = supabase.table("cours_presences").insert({
                    "membre_id": membre["id"],
                    "chien_id": chien["id"],
                    "seance_id": seance_id,
                    "present": True
                }).execute()

                if insertion.data:
                    st.success("Présence validée.")
                    st.rerun()

