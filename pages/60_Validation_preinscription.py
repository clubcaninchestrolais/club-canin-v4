import streamlit as st
from supabase_rest import supabase
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Validation préinscription", page_icon="📝")
st.title("📝 Validation des préinscriptions")

# ---------------------------------------------------------
# Charger les cours (pour récupérer Chiots / Nouvel inscrit / Agility)
# ---------------------------------------------------------
cours_table = supabase.table("cours").select("*").execute().data
cours_dict = {c["id"]: c for c in cours_table}

# ---------------------------------------------------------
# Charger les préinscriptions
# ---------------------------------------------------------
preinscriptions = (
    supabase.table("preinscriptions")
    .select("*")
    .order("id", desc=True)
    .execute()
    .data
)

if not preinscriptions:
    st.info("Aucune préinscription en attente.")
    st.stop()

# ---------------------------------------------------------
# Affichage compact et parlant
# ---------------------------------------------------------
st.subheader("📋 Préinscriptions en attente")

for pre in preinscriptions:

    nom_complet = f"{pre.get('prenom','')} {pre.get('nom','')}"
    chien = pre.get("chien_nom", "")

    # 🟩 Type de cours (Chiots / Nouvel inscrit / Agility / Obéissance)
    cours_id = pre.get("cours_id")
    cours_type = cours_dict.get(cours_id, {}).get("nom", "Cours inconnu")

    # 🟩 Nom interne du cours (si tu veux le garder)
    cours_nom = pre.get("cours_nom", "")

    date_seance = pre.get("date_seance", "")
    heure = pre.get("heure_debut", "")
    tel = pre.get("telephone", "")
    email = pre.get("email", "")

    col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 4, 2, 3, 2])

    with col1:
        st.write(f"👤 **{nom_complet}**")

    with col2:
        st.write(f"🐶 {chien}")

    with col3:
        st.write(f"📘 **{cours_type}**")  # Chiots / Nouvel inscrit / Agility

    with col4:
        st.write(f"📅 {date_seance}")

    with col5:
        st.write(f"⏰ {heure}")

    with col6:
        if st.button("Valider", key=f"val_{pre['id']}"):
            st.session_state["pre_id"] = pre["id"]
            st.session_state["go_validation"] = True
            st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Validation d'une préinscription
# ---------------------------------------------------------
if st.session_state.get("go_validation", False):

    st.session_state["go_validation"] = False
    pre_id = st.session_state["pre_id"]

    pre_data = (
        supabase.table("preinscriptions")
        .select("*")
        .eq("id", pre_id)
        .execute()
        .data
    )

    if not pre_data:
        st.error("❌ Erreur : préinscription introuvable.")
        st.stop()

    pre = pre_data[0]

    cours_id = pre.get("cours_id")
    cours_type = cours_dict.get(cours_id, {}).get("nom", "Cours inconnu")

    st.subheader("🔍 Validation de la préinscription")

    st.write(f"👤 **{pre.get('prenom', '')} {pre.get('nom', '')}**")
    st.write(f"📧 {pre.get('email', 'Non spécifié')}")
    st.write(f"📱 {pre.get('telephone', 'Non spécifié')}")
    st.write(f"🐶 **Chien :** {pre.get('chien_nom', 'Non spécifié')}")

    st.write(f"📘 **Cours :** {cours_type}")
    st.write(f"📅 **Date :** {pre.get('date_seance', '')}")
    st.write(f"⏰ **Heure :** {pre.get('heure_debut', '')}")

    st.markdown("---")

    if st.button("Créer le membre"):

        membre_insert = {
            "nom": pre.get("nom", ""),
            "prenom": pre.get("prenom", ""),
            "email": pre.get("email", ""),
            "telephone": pre.get("telephone", ""),
            "statut": "exterieur",
            "actif": False
        }

        membre_result = (
            supabase.table("membres")
            .insert(membre_insert)
            .execute()
            .data
        )

        if not membre_result:
            st.error("❌ Impossible de créer le membre.")
            st.stop()

        membre = membre_result[0]
        membre_id = membre["id"]

        chien_insert = {
            "nom": pre.get("chien_nom", "Chien"),
            "membre_id": membre_id
        }

        chien_result = (
            supabase.table("chiens")
            .insert(chien_insert)
            .execute()
            .data
        )

        if not chien_result:
            st.error("❌ Impossible de créer le chien.")
            st.stop()

        supabase.table("preinscriptions").delete().eq("id", pre_id).execute()

        st.success("🎉 Membre et chien créés avec succès.")
        st.info("Ce membre est extérieur. Il doit encore : cotisation → abonnement → présence.")
        st.rerun()

