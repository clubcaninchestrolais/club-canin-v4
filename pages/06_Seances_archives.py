import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase import create_client

st.set_page_config(page_title="Séances archivées", page_icon="📚")

st.title("📚 Séances archivées")

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# ---------------------------------------------------------
# Charger les cours
# ---------------------------------------------------------
cours_dict = {
    c["id"]: c
    for c in supabase.table("cours").select("*").execute().data
}

# ---------------------------------------------------------
# Charger les séances archivées (actif = FALSE)
# ---------------------------------------------------------
seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("actif", False)
    .order("date_seance", desc=True)
    .execute()
    .data
)

if not seances:
    st.info("Aucune séance archivée.")
    st.stop()

# ---------------------------------------------------------
# Affichage du détail si sélectionné
# ---------------------------------------------------------
seance_detail = st.session_state.get("seance_detail", None)

if seance_detail:

    s = seance_detail
    cours = cours_dict.get(s["cours_id"], {})

    st.subheader("🔍 Détail de la séance")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"📅 **Date** : {s['date_seance']}")
        st.write(f"📝 **Note** : {s.get('note', 'Aucune note')}")

    with col2:
        st.write(f"🐾 **Cours** : {cours.get('nom', 'Cours inconnu')}")
        st.write(f"👤 **Instructeur** : {cours.get('instructeur', 'Non défini')}")
        st.write(f"📌 **Niveau** : {cours.get('niveau', 'Non défini')}")

    # Présences
    presences = (
        supabase.table("cours_presences")
        .select("*")
        .eq("seance_id", s["id"])
        .execute()
        .data
    )

    st.write(f"👥 **Présences : {len(presences)}**")

    with st.expander("Voir les présences"):
        for p in presences:
            membre = (
                supabase.table("membres")
                .select("*")
                .eq("id", p["membre_id"])
                .execute()
                .data
            )
            chien = (
                supabase.table("chiens")
                .select("*")
                .eq("id", p["chien_id"])
                .execute()
                .data
            )

            membre_nom = (
                f"{membre[0]['prenom']} {membre[0]['nom']}"
                if membre else "Membre inconnu"
            )
            chien_nom = chien[0]["nom"] if chien else "Chien inconnu"

            st.write(f"• {membre_nom} — 🐶 {chien_nom} — {p['statut']}")

    st.markdown("---")

# ---------------------------------------------------------
# LISTE DES SÉANCES ARCHIVÉES
# ---------------------------------------------------------
st.subheader("📄 Liste des séances archivées")

for s in seances:

    cours = cours_dict.get(s["cours_id"], {})
    nom_cours = cours.get("nom", "Cours inconnu")

    # Présences
    presences = (
        supabase.table("cours_presences")
        .select("*")
        .eq("seance_id", s["id"])
        .execute()
        .data
    )

    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

    col1.write(f"📅 {s['date_seance']}")
    col2.write(f"🐾 {nom_cours}")
    col3.write(f"📝 Note : {s.get('note', '—')}")
    col4.write(f"👥 {len(presences)} présents")

    if col4.button("Voir", key=f"voir_{s['id']}"):
        st.session_state["seance_detail"] = s

    st.markdown("---")
