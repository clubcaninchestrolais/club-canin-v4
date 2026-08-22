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
# PDF PRO
# ---------------------------------------------------------
st.subheader("📄 Export PDF — Préinscrits par séance (version PRO)")

if st.button("📄 Télécharger la liste des préinscrits (PDF)"):

    # Regroupement par séance reconstruite
    seances_dict_pdf = {}

    for pre in preinscriptions:
        cours_nom = cours_dict.get(pre.get("cours_id"), {}).get("nom", "Cours inconnu")
        date_seance = pre.get("date_seance", "")
        heure = pre.get("heure_debut", "")

        # 🔥 Référence séance reconstruite
        nom_seance = f"{cours_nom} - {date_seance} {heure}".strip()

        # Nettoyage Unicode
        nom_seance = nom_seance.replace("—", "-")

        seances_dict_pdf.setdefault(nom_seance, []).append(pre)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, "Liste des preinscrits par seance", ln=True)
    pdf.ln(5)

    for nom_seance, liste in seances_dict_pdf.items():

        # Titre séance
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"Seance : {nom_seance}", ln=True)
        pdf.ln(2)

        # En-tête tableau
        pdf.set_font("Arial", "B", 11)
        pdf.cell(10, 8, " ", border=0)
        pdf.cell(10, 8, "N°", border=0)
        pdf.cell(60, 8, "Nom du membre", border=0)
        pdf.cell(50, 8, "Chien", border=0)
        pdf.ln(6)

        pdf.set_font("Arial", size=11)

        # Lignes tableau
        for idx, pre in enumerate(liste, start=1):
            membre_nom = f"{pre.get('prenom','')} {pre.get('nom','')}".replace("—", "-")
            chien_nom = pre.get("chien_nom", "Chien").replace("—", "-")

            pdf.cell(10, 6, "[ ]", border=0)
            pdf.cell(10, 6, f"{idx:02d}", border=0)
            pdf.cell(60, 6, membre_nom, border=0)
            pdf.cell(50, 6, chien_nom, border=0)
            pdf.ln(6)

        pdf.ln(4)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 8, f"Total inscrits : {len(liste)}", ln=True)
        pdf.ln(6)

    # Export
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
# Affichage compact (restauré)
# ---------------------------------------------------------
st.subheader("📋 Préinscriptions (affichage uniquement)")

for pre in preinscriptions:

    nom_complet = f"{pre.get('prenom','')} {pre.get('nom','')}"
    chien = pre.get("chien_nom", "")
    cours_nom = cours_dict.get(pre.get("cours_id"), {}).get("nom", "Cours inconnu")
    date_seance = pre.get("date_seance", "")
    heure = pre.get("heure_debut", "")

    bg = "background-color: #d4f8d4;" if pre.get("traitee") else "background-color: #f8e6d4;"

    st.markdown(
        f"""
        <div style="{bg}; padding:10px; border-radius:8px; margin-bottom:8px;">
            <b>👤 {nom_complet}</b><br>
            🐶 {chien}<br>
            📘 {cours_nom}<br>
            📅 {date_seance} — ⏰ {heure}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.button("Valider (affichage uniquement)", key=f"val_{pre['id']}")

st.markdown("---")

st.info("⚠️ Mode affichage uniquement — validation réelle désactivée car supabase_rest ne supporte pas les insert/update.")



