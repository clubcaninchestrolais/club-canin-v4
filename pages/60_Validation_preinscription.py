import streamlit as st
from supabase_rest import supabase
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
# PDF — Liste des préinscrits par cours
# ---------------------------------------------------------
st.subheader("📄 Export PDF — Préinscrits par cours")

if st.button("📄 Télécharger la liste des préinscrits (PDF)"):

    cours_dict = {}

    for pre in preinscriptions:
        cours_txt = pre.get("cours_nom", "Cours inconnu")

        if cours_txt not in cours_dict:
            cours_dict[cours_txt] = []

        cours_dict[cours_txt].append(pre)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Liste des preinscrits par cours", ln=True)
    pdf.ln(5)

    for cours_nom, liste in cours_dict.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"Cours : {cours_nom}", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.ln(2)

        for pre in liste:
            membre_nom = f"{pre.get('prenom','')} {pre.get('nom','')}"
            chien_nom = pre.get("chien_nom", "Chien")
            pdf.cell(0, 6, f"- {membre_nom} - Chien : {chien_nom}", ln=True)

        pdf.ln(4)

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
# Affichage compact et parlant
# ---------------------------------------------------------
st.subheader("📋 Préinscriptions en attente")

for pre in preinscriptions:

    nom_complet = f"{pre.get('prenom','')} {pre.get('nom','')}"
    chien = pre.get("chien_nom", "")
    cours = pre.get("cours_nom", "Cours inconnu")
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
        st.write(f"📘 {cours}")

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

    st.subheader("🔍 Validation de la préinscription")

    st.write(f"👤 **{pre.get('prenom', '')} {pre.get('nom', '')}**")
    st.write(f"📧 {pre.get('email', 'Non spécifié')}")
    st.write(f"📱 {pre.get('telephone', 'Non spécifié')}")
    st.write(f"🐶 **Chien :** {pre.get('chien_nom', 'Non spécifié')}")

    st.write(f"📘 **Cours :** {pre.get('cours_nom', 'Cours inconnu')}")
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

