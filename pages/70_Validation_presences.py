import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase
from datetime import datetime

st.set_page_config(page_title="Validation des présences", page_icon="🟢")
st.title("🟢 Validation des présences")

# ---------------------------------------------------------
# Initialiser la séance sélectionnée
# ---------------------------------------------------------
if "seance_detail" not in st.session_state:
    st.session_state["seance_detail"] = None

# ---------------------------------------------------------
# Charger les cours
# ---------------------------------------------------------
cours = (
    supabase.table("cours")
    .select("*")
    .execute()
    .data
)
cours_dict = {c["id"]: c for c in cours}

# ---------------------------------------------------------
# Charger les séances actives
# ---------------------------------------------------------
seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("actif", True)
    .order("date_seance", desc=False)
    .execute()
    .data
)

# ---------------------------------------------------------
# Si une séance est sélectionnée → afficher les inscrits
# ---------------------------------------------------------
if st.session_state["seance_detail"]:

    s = st.session_state["seance_detail"]
    cours_info = cours_dict.get(s["cours_id"], {})

    st.subheader("🔍 Détail de la séance")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"📅 **Date** : {s['date_seance']}")
        st.write(f"📝 **Note** : {s.get('note', 'Aucune note')}")
    with col2:
        st.write(f"🐾 **Cours** : {cours_info.get('nom', 'Cours inconnu')}")
        st.write(f"👤 **Instructeur** : {cours_info.get('instructeur', 'Non défini')}")
        st.write(f"📌 **Niveau** : {cours_info.get('niveau', 'Non défini')}")

    # ---------------------------------------------------------
    # Charger les INSCRIPTIONS DIRECTES
    # ---------------------------------------------------------
    inscrits = (
        supabase.table("cours_seances_inscriptions")
        .select("*, membres(*), chiens(*)")
        .eq("seance_id", s["id"])
        .execute()
        .data
    )

    st.markdown("---")
    st.subheader("👥 Participants à valider")

    if not inscrits:
        st.info("Aucun inscrit pour cette séance.")
        st.stop()

    for i in inscrits:

        membre = i["membres"]
        chien = i["chiens"]

        membre_nom = f"{membre['prenom']} {membre['nom']}"
        chien_nom = chien["nom"]

        colA, colB, colC = st.columns([3, 2, 2])

        with colA:
            st.write(f"- **{membre_nom}** — 🐶 {chien_nom}")

        with colB:
            if i["present"]:
                st.write("🟢 Présence validée")
            else:
                st.write("⏳ En attente de validation")

        with colC:
            if not i["present"]:
                if st.button("Valider présence", key=f"presence_{i['id']}"):

                    # ---------------------------------------------------------
                    # Vérifier cotisation + abonnement
                    # ---------------------------------------------------------
                    cotisations = (
                        supabase.table("cotisations")
                        .select("*")
                        .eq("membre_id", membre["id"])
                        .execute()
                        .data
                    )

                    cot_active = [
                        c for c in cotisations
                        if c["date_expiration"] and datetime.fromisoformat(c["date_expiration"]) > datetime.now()
                    ]

                    if not cot_active:
                        st.error("❌ Cotisation non active.")
                        st.stop()

                    abo = (
                        supabase.table("abonnements")
                        .select("*")
                        .eq("membre_id", membre["id"])
                        .eq("actif", True)
                        .execute()
                        .data
                    )

                    if not abo:
                        st.error("❌ Abonnement non actif.")
                        st.stop()

                    abonnement = abo[0]

                    if abonnement["seances_restantes"] <= 0:
                        st.error("❌ Plus de séances disponibles.")
                        st.stop()

                    # Décrémenter l'abonnement
                    supabase.table("abonnements").update({
                        "seances_restantes": abonnement["seances_restantes"] - 1
                    }).eq("id", abonnement["id"]).execute()

                    # ---------------------------------------------------------
                    # Insérer présence réelle
                    # ---------------------------------------------------------
                    supabase.table("cours_presences").insert({
                        "seance_id": s["id"],
                        "membre_id": membre["id"],
                        "chien_id": chien["id"],
                        "date_presence": s["date_seance"],
                        "present": True
                    }).execute()

                    # ---------------------------------------------------------
                    # Marquer l'inscription comme validée
                    # ---------------------------------------------------------
                    supabase.table("cours_seances_inscriptions").update({
                        "present": True
                    }).eq("id", i["id"]).execute()

                    st.success(f"Présence validée pour {membre_nom}.")
                    st.rerun()

    st.markdown("---")

# ---------------------------------------------------------
# Liste des séances actives
# ---------------------------------------------------------
st.subheader("📅 Séances actives")

for s in seances:

    cours_info = cours_dict.get(s["cours_id"], {})
    nom_cours = cours_info.get("nom", "Cours inconnu")

    col1, col2, col3 = st.columns([2, 2, 1])

    col1.write(f"📅 {s['date_seance']}")
    col2.write(f"🐾 {nom_cours}")

    if col3.button("Valider", key=f"voir_{s['id']}"):
        st.session_state["seance_detail"] = s
        st.rerun()

    st.markdown("---")
