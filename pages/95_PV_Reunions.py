# ---------------------------------------------------------
# Génération PDF via FPDF (compatible Streamlit Cloud)
# ---------------------------------------------------------

pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Logo du club
try:
    pdf.image("logo_club.png", x=10, y=8, w=30)
except:
    pass

pdf.set_font("Arial", "B", 16)
pdf.ln(25)  # espace sous le logo
pdf.cell(0, 10, f"PV de réunion - {pv['date_reunion']}", ln=True)

pdf.set_font("Arial", "", 12)
pdf.ln(5)
pdf.cell(0, 10, f"Titre : {pv['titre']}", ln=True)
pdf.cell(0, 10, f"Auteur : {pv['auteur']}", ln=True)
pdf.cell(0, 10, f"Créé le : {pv['date_creation']}", ln=True)

pdf.ln(10)
pdf.set_font("Arial", "", 11)

for line in pv["contenu"].split("\n"):
    pdf.multi_cell(0, 8, line)

# Export PDF
buffer = io.BytesIO()
pdf.output(buffer)
buffer.seek(0)

st.download_button(
    label="📄 Télécharger le PV en PDF",
    data=buffer,
    file_name=f"PV_{pv['date_reunion']}.pdf",
    mime="application/pdf"
)
