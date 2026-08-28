import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase
from datetime import date
from menu import hide_streamlit_menu, menu_lateral

st.set_page_config(page_title="Cours du jour", page_icon="📅")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("📅 Cours du jour")

# ---------------------------------------------------------
# 1. Trouver la prochaine séance ACTIVE (version blindée)
# ---------------------------------------------------------

today = date.today().isoformat()

seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("actif", True)                      # <-- uniquement séances actives
    .not_("date_seance", "is", None)        # <-- exclut NULL
    .not_("date_seance", "eq", "")          # <-- exclut vide
    .gte("date_seance", today)              # <-- compare seulement les dates valides
    .order("date_seance", desc=False)
    .limit(1)
    .execute()
    .data
)

if not seances:
    st.warning("Aucune séance future active trouvée.")
    st.stop()

seance = seances[0]
st.subheader(f"Séance du {seance['date_seance']}")

# ---------------------------------------------------------
# 2. Charger le cours lié à cette séance
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 3. INSCRIPTION DIRECTE À LA SÉANCE
# ---------------------------------------------------------
st.markdown("### ➕ Inscrire un chien à cette séance")

# Charger les membres
membres = (
    supabase.table("membres")
    .select("*")
    .order("prenom")
    .execute()
    .data
)

membre_select = st.selectbox(
    "Choisir un membre",
    membres,
    format_func=lambda m: f"{m['prenom']} {m['nom']}"
)

# Charger les chiens du membre
chiens = (
    supabase.table("chiens")
    .select("*")
    .eq("id_membre", membre_select["id"])
    .execute()
    .data
)

if not chiens:
    st.info("Ce membre n'a aucun chien enregistré.")
else:
    chien_select = st.selectbox(
        "Choisir un chien",
        chiens,
        format_func=lambda c: f"{c['nom']} ({c['race']})"
    )

    # Vérifier si déjà inscrit
    deja_inscrit = (
        supabase.table("cours_seances_inscriptions")
        .select("*")
        .eq("seance_id", seance["id"])
        .eq("chien_id", chien_select["id"])
        .execute()
        .data
    )

    if deja_inscrit:
        st.warning("⚠️ Ce chien est déjà inscrit à cette séance.")
    else:
        if st.button("Inscrire ce chien"):
            supabase.table("cours_seances_inscriptions").insert({
                "seance_id": seance["id"],
                "membre_id": membre_select["id"],
                "chien_id": chien_select["id"],
                "present": False,
                "actif": True
            }).execute()

            st.success(f"🐶 {chien_select['nom']} a été inscrit à la séance.")
            st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# 4. Charger les inscrits via cours_seances_inscriptions
# ---------------------------------------------------------
inscrits = (
    supabase.table("cours_seances_inscriptions")
    .select("*, membres(*), chiens(*)")
    .eq("seance_id", seance["id"])
    .execute()
    .data
)

st.markdown("### 👥 Chiens inscrits")

if not inscrits:
    st.write("Aucun inscrit pour cette séance.")
    st.stop()

# ---------------------------------------------------------
# 5. Afficher les inscrits
# ---------------------------------------------------------
for i in inscrits:
    membre = i["membres"]
    chien = i["chiens"]

    st.write(
        f"- **{membre['prenom']} {membre['nom']}** — "
        f"{chien['nom']} ({chien['race']})"
    )
