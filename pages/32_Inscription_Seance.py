import streamlit as st
from datetime import date
from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

# --- Sécurité ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="Inscription séance", page_icon="🐾")

hide_streamlit_menu()
menu_lateral()

st.title("🐾 Inscription à une séance")

# ---------------------------------------------------------
# Vérifier si seance_id existe
# ---------------------------------------------------------
seance_id = st.session_state.get("seance_id")

if not seance_id:
    st.warning("Aucune séance sélectionnée. Choisissez une séance ci-dessous.")

    seances = (
        supabase.table("cours_seances")
        .select("*")
        .order("date_seance", desc=False)
        .execute()
        .data
    )

    choix = st.selectbox(
        "Séance :", 
        seances, 
        format_func=lambda s: f"{s['nom_seance']} — {s['date_seance']}"
    )

    seance_id = choix["id"]
    st.session_state["seance_id"] = seance_id

st.markdown("---")

# ---------------------------------------------------------
# Charger la séance
# ---------------------------------------------------------
seance = (
    supabase.table("cours_seances")
    .select("*")
    .eq("id", seance_id)
    .execute()
    .data[0]
)

st.subheader(f"Séance : {seance['nom_seance']} — {seance['date_seance']}")
st.markdown("---")

# ---------------------------------------------------------
# Sélection du membre
# ---------------------------------------------------------
membres = (
    supabase.table("membres")
    .select("*")
    .eq("actif", True)
    .order("nom")
    .execute()
    .data
)

membre = st.selectbox("Sélectionnez un membre :", membres, format_func=lambda m: f"{m['prenom']} {m['nom']}")

# ---------------------------------------------------------
# Sélection du chien (id_membre)
# ---------------------------------------------------------
chiens = (
    supabase.table("chiens")
    .select("*")
    .eq("id_membre", membre["id"])
    .execute()
    .data
)

if not chiens:
    st.error("⛔ Ce membre n'a aucun chien actif. Impossible d'inscrire à une séance.")
    st.stop()

chien = st.selectbox("Sélectionnez un chien :", chiens, format_func=lambda c: c["nom"])

# ---------------------------------------------------------
# Vérification abonnement (id_membre)
# ---------------------------------------------------------
abo = (
    supabase.table("abonnements")
    .select("*")
    .eq("id_membre", membre["id"])
    .order("id", desc=True)
    .execute()
    .data
)

if not abo:
    st.error("Ce membre n'a aucun abonnement.")
    st.stop()

abo = abo[0]

if abo["seances_total"] != -1 and abo["seances_restantes"] <= 0:
    st.error("⛔ Abonnement épuisé.")
    st.stop()

# ---------------------------------------------------------
# Inscription
# ---------------------------------------------------------
if st.button("📝 Inscrire à cette séance"):

    # Vérifier doublon
    deja = (
        supabase.table("cours_presences")
        .select("*")
        .eq("id_membre", membre["id"])
        .eq("id_seance", seance_id)
        .execute()
        .data
    )

    if deja:
        st.warning("Ce membre est déjà inscrit à cette séance.")
        st.stop()

    supabase.table("cours_presences").insert({
        "id_membre": membre["id"],     # <-- CORRECTION
        "id_chien": chien["id"],       # <-- CORRECTION
        "id_seance": seance_id,        # <-- CORRECTION
        "date_presence": seance["date_seance"],
        "present": False,
        "statut": "absent"
    }).execute()

    st.success("Inscription enregistrée !")
    st.rerun()
