import streamlit as st
from supabase_rest import supabase
from datetime import datetime

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="Validation des présences", page_icon="📋")
st.title("📋 Validation des présences du jour")

# ---------------------------------------------------------
# 1. Charger la séance du jour
# ---------------------------------------------------------
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

st.subheader(f"Séance du {seance['date_seance']} — {seance['cours_nom']}")

# ---------------------------------------------------------
# 2. Charger les présences (membres + extérieurs)
# ---------------------------------------------------------
presences = (
    supabase.table("cours_seances_inscriptions")
    .select("*, membres(nom, prenom, statut), chiens(nom)")
    .eq("seance_id", seance_id)
    .execute()
    .data
)

if not presences:
    st.info("Aucune présence à valider.")
    st.stop()

# ---------------------------------------------------------
# 3. Affichage des présences
# ---------------------------------------------------------
for p in presences:
    st.markdown("---")

    membre = p.get("membres")
    chien = p.get("chiens")

    membre_nom = membre["nom"] if membre else "Extérieur"
    membre_prenom = membre["prenom"] if membre else ""
    chien_nom = chien["nom"] if chien else "Chien extérieur"

    st.write(f"👤 **{membre_prenom} {membre_nom}** — 🐶 {chien_nom}")

    # Déterminer si c'est un extérieur
    est_exterieur = (membre is None) or (membre.get("statut") == "exterieur")

    # ---------------------------------------------------------
    # 4. Validation de présence
    # ---------------------------------------------------------
    if not p["present"]:
        if st.button(f"Valider présence #{p['id']}", key=f"valider_{p['id']}"):

            # ---------------------------------------------------------
            # CAS 1 : EXTÉRIEUR → autorisé sans cotisation ni abonnement
            # ---------------------------------------------------------
            if est_exterieur:
                supabase.table("cours_seances_inscriptions").update({
                    "present": True
                }).eq("id", p["id"]).execute()

                st.success("Présence validée (extérieur).")
                st.rerun()

            # ---------------------------------------------------------
            # CAS 2 : MEMBRE → vérifier cotisation + abonnement
            # ---------------------------------------------------------
            else:
                # Vérifier cotisation active
                cotisation = (
                    supabase.table("cotisations")
                    .select("*")
                    .eq("membre_id", p["membre_id"])
                    .eq("statut", "active")
                    .execute()
                    .data
                )

                if not cotisation:
                    st.error("❌ Cotisation non active — impossible de valider.")
                    st.stop()

                # Vérifier abonnement actif
                abo = (
                    supabase.table("abonnements")
                    .select("*")
                    .eq("membre_id", p["membre_id"])
                    .eq("actif", True)
                    .execute()
                    .data
                )

                if not abo:
                    st.error("❌ Abonnement non actif — impossible de valider.")
                    st.stop()

                abonnement = abo[0]

                if abonnement["seances_restantes"] <= 0:
                    st.error("❌ Plus de séances restantes.")
                    st.stop()

                # Décrémenter l'abonnement
                supabase.table("abonnements").update({
                    "seances_restantes": abonnement["seances_restantes"] - 1
                }).eq("id", abonnement["id"]).execute()

                # Valider la présence
                supabase.table("cours_seances_inscriptions").update({
                    "present": True
                }).eq("id", p["id"]).execute()

                st.success("Présence validée (membre).")
                st.rerun()

    else:
        st.success("Présence déjà validée.")
