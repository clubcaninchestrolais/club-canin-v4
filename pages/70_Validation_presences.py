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
    .order("id")
    .execute()
    .data
)

if not seances:
    st.info("Aucune séance aujourd'hui.")
    st.stop()

for seance in seances:

    seance_id = seance["id"]

    st.markdown(f"## 🐾 {seance['nom_seance']} — {seance['date_seance']}")

    # Membres inscrits à cette séance
    inscriptions = (
        supabase.table("cours_inscriptions")
        .select("*")
        .eq("seance_id", seance_id)
        .execute()
        .data
    )

    # Extérieurs validés pour cette séance
    exterieurs = (
        supabase.table("preinscriptions")
        .select("*")
        .eq("seance_id", seance_id)
        .eq("acceptee", True)
        .execute()
        .data
    )

    participants = []

    # Membres
    for ins in inscriptions:
        membre = supabase.table("membres").select("*").eq("id", ins["membre_id"]).execute().data
        chien = supabase.table("chiens").select("*").eq("id", ins["chien_id"]).execute().data
        if membre and chien:
            participants.append({
                "membre": membre[0],
                "chien": chien[0],
                "inscription_id": ins["id"]
            })

    # Extérieurs
    for ext in exterieurs:
        membre = supabase.table("membres").select("*").eq("id", ext["membre_id"]).execute().data
        chien = supabase.table("chiens").select("*").eq("id", ext["chien_id"]).execute().data
        if membre and chien:
            participants.append({
                "membre": membre[0],
                "chien": chien[0],
                "inscription_id": ext["id"]
            })

    if not participants:
        st.warning("Aucun inscrit pour cette séance.")
        continue

    # Affichage + validation
    for p in participants:

        membre = p["membre"]
        chien = p["chien"]

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
                🐶 {chien['nom']}
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

                st.success("Présence validée.")
                st.rerun()

        else:
            st.success("Présence déjà validée.")
