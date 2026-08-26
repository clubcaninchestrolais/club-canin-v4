import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# Sécurité
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

# Connexion Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Validation des présences du jour")

# Charger la séance du jour
aujourdhui = datetime.now().date().isoformat()

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

st.subheader(f"Séance du {seance['date_seance']} — {seance.get('nom_seance', 'Séance')}")

# Charger les présences
try:
    presences = (
        supabase.table("cours_seances_inscriptions")
        .select("*")
        .eq("seance_id", seance_id)
        .execute()
        .data
    )
except Exception:
    st.error("❌ Erreur lors du chargement des présences.")
    st.stop()

if not presences:
    st.info("Aucune présence à valider.")
    st.stop()

# Affichage des présences
for p in presences:
    st.markdown("---")

    est_exterieur = (p.get("type_inscription") == "exterieur")

    # EXTÉRIEUR — ultra simple, zéro requête
    if est_exterieur:
        nom_ext = p.get("nom_exterieur", "Extérieur")
        prenom_ext = p.get("prenom_exterieur", "")
        chien_ext = p.get("chien_exterieur", "Chien extérieur")

        st.write(f"👤 {prenom_ext} {nom_ext} — 🐶 {chien_ext}")

    else:
        # MEMBRE
        membre = None
        if p.get("membre_id"):
            membre_data = (
                supabase.table("membres")
                .select("*")
                .eq("id", p["membre_id"])
                .execute()
                .data
            )
            membre = membre_data[0] if membre_data else None

        chien = None
        if p.get("chien_id"):
            chien_data = (
                supabase.table("chiens")
                .select("*")
                .eq("id", p["chien_id"])
                .execute()
                .data
            )
            chien = chien_data[0] if chien_data else None

        membre_nom = membre["nom"] if membre else "Membre inconnu"
        membre_prenom = membre["prenom"] if membre else ""
        chien_nom = chien["nom"] if chien else "Chien inconnu"

        st.write(f"👤 {membre_prenom} {membre_nom} — 🐶 {chien_nom}")

    # Validation de présence
    if not p["present"]:
        if st.button(f"Valider présence #{p['id']}", key=f"valider_{p['id']}"):

            # EXTÉRIEUR
            if est_exterieur:
                supabase.table("cours_seances_inscriptions").update({
                    "present": True
                }).eq("id", p["id"]).execute()

                st.success("Présence validée (extérieur).")
                st.rerun()

            # MEMBRE
            else:
                cotisation = (
                    supabase.table("cotisations")
                    .select("*")
                    .eq("membre_id", p["membre_id"])
                    .eq("statut", "active")
                    .execute()
                    .data
                )

                if not cotisation:
                    st.error("❌ Cotisation non active.")
                    st.stop()

                abo = (
                    supabase.table("abonnements")
                    .select("*")
                    .eq("membre_id", p["membre_id"])
                    .eq("actif", True)
                    .execute()
                    .data
                )

                if not abo:
                    st.error("❌ Abonnement non actif.")
                    st.stop()

                abonnement = abo[0]

                if abonnement["seances_restantes"] <= 0:
                    st.error("❌ Plus de séances restantes.")
                    st.stop()

                supabase.table("abonnements").update({
                    "seances_restantes": abonnement["seances_restantes"] - 1
                }).eq("id", abonnement["id"]).execute()

                supabase.table("cours_seances_inscriptions").update({
                    "present": True
                }).eq("id", p["id"]).execute()

                st.success("Présence validée (membre).")
                st.rerun()

    else:
        st.success("Présence déjà validée.")
