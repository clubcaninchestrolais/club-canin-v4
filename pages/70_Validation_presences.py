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

# Regrouper les séances par cours
cours_groupes = {}
for s in seances:
    cid = s["cours_id"]
    cours_groupes.setdefault(cid, []).append(s)

# Parcours des cours du jour
for cours_id, liste_seances in cours_groupes.items():

    # 🔥 Sécurité : ignorer les cours inexistants
    if cours_id not in cours_dict:
        st.warning(f"Cours ID {cours_id} introuvable dans la table 'cours'. Séance ignorée.")
        continue

    cours_nom = cours_dict[cours_id]["nom_cours"]
    st.markdown(f"## 🐾 {cours_nom}")

    # Charger les inscriptions membres
    inscriptions = (
        supabase.table("cours_inscriptions")
        .select("*")
        .eq("cours_id", cours_id)
        .execute()
        .data
    )

    # Charger les extérieurs validés
    exterieurs = (
        supabase.table("preinscriptions")
        .select("*")
        .eq("cours_id", cours_id)
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
                "seance_id": ins["seance_id"],
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
                "seance_id": ext["seance_id"],
                "inscription_id": ext["id"]
            })

    if not participants:
        st.warning("Aucun inscrit pour ce cours.")
        continue

    # 🔥 AFFICHAGE + VALIDATION
    for p in participants:

        membre = p["membre"]
        chien = p["chien"]
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
                Séance ID : {seance_id}
            </div>
            """,
            unsafe_allow_html=True
        )

        if not deja:
            if st.button(
                f"Valider présence de {membre['prenom']} {membre['nom']}",
                key=f"btn_{p['inscription_id']}"
            ):
                # Enregistrer la présence
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
