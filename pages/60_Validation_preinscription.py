import streamlit as st
from supabase_rest import supabase
from datetime import datetime
from fpdf import FPDF
from io import BytesIO

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
# PDF — Liste des préinscrits par cours (version ASCII-safe)
# ---------------------------------------------------------
st.subheader("📄 Export PDF — Préinscrits par cours")

if st.button("📄 Télécharger la liste des préinscrits (PDF)"):

    # Regrouper par cours
    cours_dict = {}

    for pre in preinscriptions:
        cours_txt = (
            pre.get("cours_demande")
            or pre.get("cours")
            or pre.get("cours_id")
            or "Non specifie"
        )

        if cours_txt not in cours_dict:
            cours_dict[cours_txt] = []

        cours_dict[cours_txt].append(pre)

    # Création du PDF (Arial ASCII-safe)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Liste des preinscrits par cours", ln=True)
    pdf.ln(5)

    for cours_nom, liste in cours_dict.items():
        pdf.set_font("Arial", "B", 12)
        cours_ascii = cours_nom.encode("ascii", "ignore").decode()
        pdf.cell(0, 8, f"Cours : {cours_ascii}", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.ln(2)

        for pre in liste:
            membre_nom = f"{pre.get('prenom', '')} {pre.get('nom', '')}"
            chien_nom = pre.get("chien_nom", "Chien")

            # Conversion ASCII-safe (accents supprimés automatiquement)
            membre_ascii = membre_nom.encode("ascii", "ignore").decode()
            chien_ascii = chien_nom.encode("ascii", "ignore").decode()

            pdf.cell(0, 6, f"- {membre_ascii} - Chien : {chien_ascii}", ln=True)

        pdf.ln(4)

    # Export PDF
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="📄 Télécharger PDF",
        data=pdf_buffer,
        file_name="preinscrits.pdf",
        mime="application/pdf"
    )

st.markdown("---")

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

