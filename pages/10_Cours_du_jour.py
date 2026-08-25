import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase
from datetime import date
from menu import hide_streamlit_menu, menu_lateral   # <-- AJOUT

st.set_page_config(page_title="Cours du jour", page_icon="📅")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()   # <-- AJOUT

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()          # <-- AJOUT

st.title("📅 Cours du jour")

# 1. Trouver la prochaine séance (date_seance)
seances = (
    supabase.table("cours_seances")
    .select("*")
    .gte("date_seance", date.today().isoformat())
    .order("date_seance", desc=False)
    .limit(1)
    .execute()
    .data
)

if not seances:
    st.warning("Aucune séance future trouvée.")
    st.stop()

seance = seances[0]
st.subheader(f"Séance du {seance['date_seance']}")

# 2. Charger le cours lié à cette séance
cours = (
    supabase.table("cours")
    .select("*")
    .eq("id", seance["cours_id"])
    .execute()
    .data
)

if not cours:
    st.info("Aucun cours trouvé pour cette séance.")
    st.stop()

cours = cours[0]

st.markdown("---")
st.write(f"### 🐾 {cours['categorie']} (ID {cours['id']})")

# 3. Charger les inscrits via cours_seances_inscriptions
inscrits = (
    supabase.table("cours_seances_inscriptions")
    .select("*, membres(*), chiens(*)")
    .eq("seance_id", seance["id"])
    .execute()
    .data
)

if not inscrits:
    st.write("Aucun inscrit pour cette séance.")
    st.stop()

# 4. Afficher les inscrits
for i in inscrits:
    membre = i["membres"]
    chien = i["chiens"]

    st.write(
        f"- **{membre['prenom']} {membre['nom']}** — "
        f"{chien['nom']} ({chien['race']})"
    )
