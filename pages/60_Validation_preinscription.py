import streamlit as st
from supabase_rest import supabase

st.set_page_config(page_title="Validation préinscriptions", page_icon="📝")
st.title("📝 Validation des préinscriptions (NON-MEMBRES)")

# ---------------------------------------------------------
# Charger les préinscriptions
# ---------------------------------------------------------
pre_table = supabase.table("preinscriptions").select("*").order("id", desc=True).execute()
preinscriptions = pre_table.data or []

# Filtrer UNIQUEMENT les non-membres
non_membres = [p for p in preinscriptions if p.get("membre_id") is None]

if not non_membres:
    st.info("Aucun non-membre en préinscription.")
    st.stop()

# ---------------------------------------------------------
# Affichage des non-membres avec boutons VALIDER / REFUSER
# ---------------------------------------------------------
st.subheader("👤 Non-membres préinscrits")

for pre in non_membres:

    nom_complet = f"{pre.get('prenom','')} {pre.get('nom','')}"
    chien = pre.get("chien_nom", "")
    cours_nom = pre.get("cours_nom", "Cours inconnu")
    date_seance = pre.get("date_seance", "")
    heure = pre.get("heure_debut", "")

    statut = pre.get("statut_preinscription", "en_attente")

    # Couleur selon statut
    if statut == "valide":
        bg = "background-color: #d4f8d4;"  # vert clair
    elif statut == "refuse":
        bg = "background-color: #f8d4d4;"  # rouge clair
    else:
        bg = "background-color: #f8f3d4;"  # jaune clair

    st.markdown(
        f"""
        <div style="{bg}; padding:12px; border-radius:8px; margin-bottom:10px;">
            <b>👤 {nom_complet}</b><br>
            🐶 {chien}<br>
            📘 {cours_nom}<br>
            📅 {date_seance} — ⏰ {heure}<br>
            <i>Statut : {statut}</i>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"VALIDER {nom_complet}", key=f"val_{pre['id']}"):
            supabase.table("preinscriptions").update({"statut_preinscription": "valide"}).eq("id", pre["id"]).execute()
            st.rerun()

    with col2:
        if st.button(f"REFUSER {nom_complet}", key=f"ref_{pre['id']}"):
            supabase.table("preinscriptions").update({"statut_preinscription": "refuse"}).eq("id", pre["id"]).execute()
            st.rerun()

st.markdown("---")
st.info("Cette page prépare la séance : seuls les NON-MEMBRES sont affichés. La validation réelle se fera dans la page 'Validation des présences'.")




