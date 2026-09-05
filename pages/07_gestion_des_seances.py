import streamlit as st
from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="gestion des seances", page_icon="📅")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("📅 Gestion des séances")
st.markdown("---")

# ---------------------------------------------------------
# Filtre : afficher les séances archivées ?
# ---------------------------------------------------------
afficher_archives = st.toggle("Afficher les séances archivées", value=False)

# ---------------------------------------------------------
# Charger TOUTES les séances
# ---------------------------------------------------------
query = supabase.table("cours_seances").select("*")

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
        st.info("Aucune séance archivée.")
    else:
        st.info("Aucune séance active.")
    st.stop()

# ---------------------------------------------------------
# Affichage des séances
# ---------------------------------------------------------
for seance in seances:

    with st.container():
        statut = "🟢 Active" if seance["actif"] else "📦 Archivée"
        st.write(f"📅 **{seance['date_seance']}** — {statut}")

        # Charger le cours pour afficher son nom
        cours = (
            supabase.table("cours")
            .select("*")
            .eq("id", seance["cours_id"])
            .execute()
            .data[0]
        )

        st.write(f"📘 **Cours : {cours['nom']}**")

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
