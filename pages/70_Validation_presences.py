import streamlit as st
from supabase import create_client, Client
import datetime

# Connexion Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Validation des présences")

# Séance du jour
aujourdhui = datetime.date.today().isoformat()

seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("date_seance", aujourdhui)
    .execute()
    .data
)

if not seances:
    st.info("Aucune séance aujourd'hui.")
    st.stop()

seance = seances[0]
seance_id = seance["id"]

st.subheader(f"Séance du jour : {seance['nom_seance']}")

# ---------------------------------------------------------
# 1️⃣ EXTÉRIEURS VALIDÉS
# ---------------------------------------------------------
exterieurs = (
    supabase.table("preinscriptions")
    .select("*")
    .eq("seance_id", seance_id)
    .eq("acceptee", True)
    .execute()
    .data
)

# ---------------------------------------------------------
# 2️⃣ MEMBRES INSCRITS
# ---------------------------------------------------------
inscriptions = (
    supabase.table("cours_seances_inscriptions")
    .select("*")
    .eq("seance_id", seance_id)
    .eq("actif", True)
    .execute()
    .data
)

membres_inscrits = []
for ins in inscriptions:
    membre = (
        supabase.table("membres")
        .select("*")
        .eq("id", ins["membre_id"])
        .execute()
        .data
    )
    chien = (
        supabase.table("chiens")
        .select("*")
        .eq("id", ins["chien_id"])
        .execute()
        .data
    )

    if membre and chien:
        membres_inscrits.append({
            "inscription_id": ins["id"],
            "membre": membre[0],
            "chien": chien[0]
        })

# ---------------------------------------------------------
# 3️⃣ AFFICHAGE FUSIONNÉ
# ---------------------------------------------------------
st.markdown("### Participants à valider")

# ---------------------------------------------------------
# EXTÉRIEURS — OPTION B
# ---------------------------------------------------------
for ext in exterieurs:
    st.write(f"🟦 Extérieur : {ext['prenom']} {ext['nom']} – {ext['chien_nom']}")

    if st.button(f"Valider présence extérieur {ext['id']}"):
        insertion = (
            supabase.table("preinscriptions")
            .update({"present_exterieur": True})
            .eq("id", ext["id"])
            .select("*")
            .execute()
        )

        if insertion.data:
            st.success("Présence extérieur validée (premier cours).")
            st.rerun()
        else:
            st.error("❌ Erreur lors de la validation.")
            st.write(insertion)

# ---------------------------------------------------------
# MEMBRES — Validation normale
# ---------------------------------------------------------
for item in membres_inscrits:
    membre = item["membre"]
    chien = item["chien"]

    st.write(f"🟩 Membre : {membre['prenom']} {membre['nom']} – {chien['nom']}")

    if st.button(f"Valider présence membre {item['inscription_id']}"):
        insertion = supabase.table("cours_presences").insert({
            "membre_id": membre["id"],      # ✔ correction
            "chien_id": chien["id"],        # ✔ correction
            "seance_id": seance_id,
            "date_presence": aujourdhui,
            "present": True
        }).execute()

        if insertion.data:
            st.success("Présence membre validée.")
            st.rerun()
        else:
            st.error("❌ Erreur lors de l'enregistrement.")
            st.write(insertion)

