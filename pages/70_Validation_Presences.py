import streamlit as st
from supabase_rest import supabase
from datetime import datetime

st.set_page_config(page_title="Validation des présences", page_icon="🟢")
st.title("🟢 Validation des présences")

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

if not seances:
    st.info("Aucune séance active.")
    st.stop()

# ---------------------------------------------------------
# Détail d'une séance
# ---------------------------------------------------------
seance_detail = st.session_state.get("seance_detail", None)

if seance_detail:

    s = seance_detail
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
    # Charger les préinscriptions validées (membres + extérieurs)
    # ---------------------------------------------------------
    preinscrits = (
        supabase.table("preinscriptions")
        .select("*")
        .eq("seance_id", s["id"])
        .eq("acceptee", True)
        .execute()
        .data
    )

    st.markdown("---")
    st.subheader("👥 Participants à valider")

    if not preinscrits:
        st.info("Aucun participant pour cette séance.")
        st.stop()

    for p in preinscrits:

        # ---------------------------------------------------------
        # Charger infos membre ou extérieur
        # ---------------------------------------------------------
        if p["type"] == "membre":
            membre = (
                supabase.table("membres")
                .select("*")
                .eq("id", p["membre_id"])
                .execute()
                .data
            )
            membre_nom = f"{membre[0]['prenom']} {membre[0]['nom']}" if membre else "Membre inconnu"

            chien = (
                supabase.table("chiens")
                .select("*")
                .eq("id", p["chien_id"])
                .execute()
                .data
            )
            chien_nom = chien[0]["nom"] if chien else "Chien inconnu"

        else:
            membre_nom = f"{p['prenom']} {p['nom']}"
            chien_nom = p["chien_nom"]

        colA, colB, colC = st.columns([3, 2, 2])

        with colA:
            st.write(f"- **{membre_nom}** — 🐶 {chien_nom} ({p['type']})")

        with colB:
            st.write("⏳ En attente de validation")

        with colC:
            if st.button("Valider présence", key=f"presence_{p['id']}"):

                # ---------------------------------------------------------
                # Membres : vérifier cotisation + abonnement
                # ---------------------------------------------------------
                if p["type"] == "membre":

                    membre_id = p["membre_id"]

                    # Cotisation
                    cotisations = (
                        supabase.table("cotisations")
                        .select("*")
                        .eq("membre_id", membre_id)
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

                    # Abonnement
                    abo = (
                        supabase.table("abonnements")
                        .select("*")
                        .eq("membre_id", membre_id)
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

                    # Décrémenter abonnement
                    supabase.table("abonnements").update({
                        "seances_restantes": abonnement["seances_restantes"] - 1
                    }).eq("id", abonnement["id"]).execute()

                # ---------------------------------------------------------
                # Insérer présence réelle
                # ---------------------------------------------------------
                supabase.table("cours_presences").insert({
                    "seance_id": s["id"],
                    "cours_id": s["cours_id"],
                    "membre_id": p.get("membre_id"),
                    "chien_id": p.get("chien_id"),
                    "type": p["type"],
                    "date_seance": s["date_seance"],
                    "present": True
                }).execute()

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
