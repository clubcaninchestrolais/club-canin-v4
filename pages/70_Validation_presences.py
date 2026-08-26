import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

# --- CONNEXION SUPABASE ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

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
nom_seance = seance.get("nom_seance", "Séance")

st.subheader(f"Séance du {seance['date_seance']} — {nom_seance}")

# ---------------------------------------------------------
# 2. Charger les présences
# ---------------------------------------------------------
presences = (
    supabase.table("cours_seances_inscriptions")
    .select("*")
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

    est_exterieur = (p.get("type_inscription") == "exterieur")

    # ---------------------------------------------------------
    # EXTÉRIEUR — VERSION ROBUSTE (NE PEUT PAS PLANTER)
    # ---------------------------------------------------------
    if est_exterieur:
        pre = (
            supabase.table("preinscriptions")
            .select("*")
            .eq("seance_id", p["seance_id"])
            .eq("type", "exterieur")
            .execute()
            .data
        )

        if pre:
            pr = pre[-1]  # dernière entrée sans order()
            nom_ext = pr.get("nom", "Extérieur")
            prenom_ext = pr.get("prenom", "")
            nom_chien_ext = pr.get("chien_nom", "Chien extérieur")
            st.write(f"👤 {prenom_ext} {nom_ext} — 🐶 {nom_chien_ext}")
        else:
            st.write("👤 Extérieur — 🐶 Chien extérieur")

    # ---------------------------------------------------------
    # MEMBRE
    # ---------------------------------------------------------
    else:
        membre = None
        if p.get("membre_id") is not None:
            membre_data = (
                supabase.table("membres")
                .select("*")
                .eq("id", p["membre_id"])
                .execute()
                .data
            )
            membre = membre_data[0] if membre_data else None

        chien = None
        if p.get("chien_id") is not None:
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

    # ---------------------------------------------------------
    # 4. Validation de présence
    # ---------------------------------------------------------
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
                    st.error("❌ Cotisation non active — impossible de valider.")
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
                    st.error("❌ Abonnement non actif — impossible de valider.")
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
