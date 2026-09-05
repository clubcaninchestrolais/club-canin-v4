import streamlit as st
from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

# --- Sécurité ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="Inscrits à la séance", page_icon="👥")

hide_streamlit_menu()
menu_lateral()

st.title("👥 Liste des inscrits à la séance")
st.markdown("---")

# ---------------------------------------------------------
# Vérifier que la séance est définie
# ---------------------------------------------------------
if "seance_id" not in st.session_state:
    st.error("Aucune séance sélectionnée.")
    st.stop()

seance_id = st.session_state["seance_id"]

# ---------------------------------------------------------
# Charger la séance
# ---------------------------------------------------------
seance = (
    supabase.table("cours_seances")
    .select("*")
    .eq("id", seance_id)
    .execute()
    .data
)

if not seance:
    st.error("Séance introuvable.")
    st.stop()

seance = seance[0]

# Charger le cours
cours = (
    supabase.table("cours")
    .select("*")
    .eq("id", seance["cours_id"])
    .execute()
    .data[0]
)

st.write(f"📅 **Date : {seance['date_seance']}**")
st.write(f"📘 **Cours : {cours['nom']}**")
st.markdown("---")

# ---------------------------------------------------------
# Charger les inscrits
# ---------------------------------------------------------
inscriptions = (
    supabase.table("seances_inscriptions")
    .select("*, chiens(*), membres(*)")
    .eq("seance_id", seance_id)
    .execute()
    .data
)

if not inscriptions:
    st.info("Aucun inscrit pour cette séance.")
    st.stop()

# ---------------------------------------------------------
# Affichage des inscrits
# ---------------------------------------------------------
for ins in inscriptions:

    chien = ins["chiens"]
    membre = ins["membres"]

    nom_chien = chien["nom"]
    nom_membre = f"{membre['prenom']} {membre['nom']}"

    statut = "🟢 Présent" if ins.get("present", False) else "⚪ Absent"

    with st.container():
        st.write(f"🐶 **{nom_chien}** — 👤 {nom_membre} — {statut}")
        st.markdown("---")
