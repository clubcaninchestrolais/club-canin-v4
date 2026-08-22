import streamlit as st
from supabase_rest import supabase
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Validation préinscription", page_icon="📝")
st.title("📝 Validation des préinscriptions")

# ---------------------------------------------------------
# Charger les cours
# ---------------------------------------------------------
cours_table = supabase.table("cours").select("*").execute()
cours_list = cours_table.data or []
cours_dict = {c["id"]: c for c in cours_list}

# ---------------------------------------------------------
# Charger les préinscriptions
# ---------------------------------------------------------
pre_table = supabase.table("preinscriptions").select("*").order("id", desc=True).execute()
preinscriptions = pre_table.data or []

if not preinscriptions:
    st.info("Aucune préinscription.")
    st.stop()

# ---------------------------------------------------------
# PDF
# ---------------------------------------------------------
st.subheader("📄 Export PDF — Préinscrits par séance")

if st.button("📄 Télécharger la liste des préinscrits (PDF)"):

    # Regroupement par nom_seance
    seances_dict_pdf = {}

    for pre in preinscriptions:
        nom_seance = pre.get("nom_seance", "Séance inconnue")
        seances_dict_pdf.setdefault(nom_seance, []).append(pre)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Liste des préinscrits par séance", ln=True)
    pdf.ln(5)

    for nom_seance, liste in seances_dict_pdf.items():

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"Séance : {nom_seance}", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.ln(2)

        # Format liste lisible
        for pre in liste:
            membre_nom = f"{pre.get('prenom','')} {pre.get('nom','')}"
            chien_nom = pre.get("chien_nom", "Chien")
            pdf.cell(0, 6, f"[ ] {membre_nom} — Chien : {chien_nom}", ln=True)

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
# Affichage compact (sans validation réelle)
# ---------------------------------------------------------
st.subheader("📋 Préinscriptions (affichage uniquement)")

for pre in preinscriptions:

    nom_complet = f"{pre.get('prenom','')} {pre.get('nom','')}"
    chien = pre.get("chien_nom", "")

    nom_seance = pre.get("nom_seance", "Séance inconnue")

    # Couleur selon état (affichage seulement)
    if pre.get("traitee"):
        bg = "background-color: #d4f8d4;"   # vert clair
    else:
        bg = "background-color: #f8e6d4;"   # orange clair

    st.markdown(
        f"""
        <div style="{bg}; padding:10px; border-radius:8px; margin-bottom:8px;">
            <b>👤 {nom_complet}</b><br>
            🐶 {chien}<br>
            📘 {nom_seance}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.button("Valider (affichage uniquement)", key=f"val_{pre['id']}")

st.markdown("---")

st.info("⚠️ Mode affichage uniquement — validation réelle désactivée car supabase_rest ne supporte pas les insert/update.")


