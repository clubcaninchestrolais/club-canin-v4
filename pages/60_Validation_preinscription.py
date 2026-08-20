import streamlit as st
from supabase_rest import supabase
from datetime import datetime

st.set_page_config(page_title="Validation préinscription", page_icon="📝")
st.title("📝 Validation des préinscriptions")

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
# Affichage des préinscriptions
# ---------------------------------------------------------
st.subheader("📋 Préinscriptions en attente")

for pre in preinscriptions:

    col1, col2, col3 = st.columns([3, 3, 2])

    with col1:
        st.write(f"👤 **{pre.get('prenom', '')} {pre.get('nom', '')}**")
        st.write(f"📧 {pre.get('email', 'Non spécifié')}")
        st.write(f"📱 {pre.get('telephone', 'Non spécifié')}")

    with col2:
        st.write(f"🐶 **Chien :** {pre.get('chien_nom', 'Non spécifié')}")
        st.write(f"📅 **Date :** {pre.get('date_preinscription', 'Non spécifié')}")

        # Champ cours demandé (sécurisé)
        cours_txt = (
            pre.get("cours_demande")
            or pre.get("cours")
            or pre.get("cours_id")
            or "Non spécifié"
        )
        st.write(f"📝 **Cours demandé :** {cours_txt}")

    with col3:
        if st.button("Valider", key=f"valider_{pre['id']}"):
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

    # Charger la préinscription
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

    st.subheader("🔍 Validation de la préinscription")

    st.write(f"👤 **{pre.get('prenom', '')} {pre.get('nom', '')}**")
    st.write(f"📧 {pre.get('email', 'Non spécifié')}")
    st.write(f"📱 {pre.get('telephone', 'Non spécifié')}")
    st.write(f"🐶 **Chien :** {pre.get('chien_nom', 'Non spécifié')}")

    cours_txt = (
        pre.get("cours_demande")
        or pre.get("cours")
        or pre.get("cours_id")
        or "Non spécifié"
    )
    st.write(f"📝 **Cours demandé :** {cours_txt}")

    st.markdown("---")

    # ---------------------------------------------------------
    # Création du membre
    # ---------------------------------------------------------
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

        # ---------------------------------------------------------
        # Création du chien
        # ---------------------------------------------------------
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

        # ---------------------------------------------------------
        # Supprimer la préinscription validée
        # ---------------------------------------------------------
        supabase.table("preinscriptions").delete().eq("id", pre_id).execute()

        st.success("🎉 Membre et chien créés avec succès.")
        st.info("Ce membre est extérieur. Il doit encore : cotisation → abonnement → présence.")
        st.rerun()

