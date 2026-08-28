import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

st.set_page_config(page_title="Séances du cours", page_icon="📅")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("📅 Séances du cours")

# ---------------------------------------------------------
# Vérifier si cours_id existe
# ---------------------------------------------------------
cours_id = st.session_state.get("cours_id")

if not cours_id:
    st.info("Sélectionnez un cours pour afficher ses séances.")

    cours_list = (
        supabase.table("cours")
        .select("*")
        .order("nom")
        .execute()
        .data
    )

    if not cours_list:
        st.error("Aucun cours disponible.")
        st.stop()

    choix = st.selectbox("Cours :", cours_list, format_func=lambda c: c["nom"])
    cours_id = choix["id"]
    st.session_state["cours_id"] = cours_id

st.markdown("---")

# ---------------------------------------------------------
# Charger le cours
# ---------------------------------------------------------
cours = (
    supabase.table("cours")
    .select("*")
    .eq("id", cours_id)
    .execute()
    .data[0]
)

st.subheader(f"Cours : {cours['nom']}")
st.markdown("---")

# ---------------------------------------------------------
# Boutons en haut
# ---------------------------------------------------------
colA, colB = st.columns(2)

with colA:
    if st.button("➕ Ajouter une séance"):
        st.switch_page("pages/06_Ajouter_Seance.py")

with colB:
    if st.button("⬅️ Retour aux cours"):
        st.switch_page("pages/04_Cours.py")

st.markdown("---")

# ---------------------------------------------------------
# Filtre : afficher les séances archivées ?
# ---------------------------------------------------------
afficher_archives = st.toggle("Afficher les séances archivées", value=False)

# ---------------------------------------------------------
# Charger les séances selon le filtre
# ---------------------------------------------------------
query = (
    supabase.table("cours_seances")
    .select("*")
    .eq("cours_id", cours_id)
)

if afficher_archives:
    query = query.eq("actif", False)
else:
    query = query.eq("actif", True)

seances = query.order("date_seance").execute().data

# ---------------------------------------------------------
# Si aucune séance
# ---------------------------------------------------------
if not seances:
    if afficher_archives:
        st.info("Aucune séance archivée pour ce cours.")
    else:
        st.info("Aucune séance active pour ce cours.")
    st.stop()

# ---------------------------------------------------------
# Affichage des séances
# ---------------------------------------------------------
for seance in seances:
    with st.container():
        statut = "🟢 Active" if seance["actif"] else "📦 Archivée"
        st.write(f"📅 **{seance['date_seance']}** — {statut}")

        col1, col2, col3, col4 = st.columns(4)

        # --- Modifier ---
        with col1:
            if st.button(f"✏️ Modifier", key=f"edit_{seance['id']}"):
                st.session_state["seance_id"] = seance["id"]
                st.switch_page("pages/08_Modifier_Seance.py")

        # --- Inscriptions ---
        with col2:
            if st.button(f"📝 Inscriptions", key=f"inscr_{seance['id']}"):
                st.session_state["seance_id"] = seance["id"]
                st.switch_page("pages/32_Inscription_Seance.py")

        # --- Archiver / Réactiver ---
        with col3:
            if seance["actif"]:
                if st.button(f"📦 Archiver", key=f"archive_{seance['id']}"):
                    supabase.table("cours_seances").update({"actif": False}).eq("id", seance["id"]).execute()
                    st.rerun()
            else:
                if st.button(f"🔄 Réactiver", key=f"reactive_{seance['id']}"):
                    supabase.table("cours_seances").update({"actif": True}).eq("id", seance["id"]).execute()
                    st.rerun()

        # --- Supprimer ---
        with col4:
            if st.button(f"🗑️ Supprimer", key=f"delete_{seance['id']}"):
                supabase.table("cours_seances").delete().eq("id", seance["id"]).execute()
                st.rerun()

        st.markdown("---")
