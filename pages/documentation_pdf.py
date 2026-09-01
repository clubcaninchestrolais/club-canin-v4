from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st
import io

def generate_pdf():
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 760, "Documentation Technique — Club Canin Chestrolais")

    pdf.setFont("Helvetica", 12)
    y = 730

    sections = [
        "1. Introduction",
        "Mission du club",
        "Objectifs du système numérique",
        "Architecture générale (Streamlit + Supabase)",
        "Rôles : membre, préposé, comité",

        "2. Flux Extérieur (Préinscriptions)",
        "Formulaire public — public_portail.py — table preinscriptions",
        "Validation — page_60_validation.py — Accepté/Refusé",
        "Transformation — page_70_transformation.py — membres, chiens, cotisations, abonnements",
        "Nettoyage automatique — trigger delete_preinscriptions()",

        "3. Flux Membre",
        "Connexion — login.py — Auth Supabase",
        "Inscription — page_80_inscription.py — table presences",
        "Présence — page_90_presence.py",
        "Décrémentation — trigger update_abonnement()",
        "Historique — page_100_historique.py",

        "4. Schémas officiels",
        "Schéma global corporate",
        "Schéma technique",
        "Schéma vertical membre",
        "Schéma horizontal global",
        "Schéma extérieur",

        "5. Sécurité & RLS Supabase",
        "RLS membres, chiens, presences, preinscriptions, abonnements, historique",

        "6. Architecture technique",
        "Structure des pages Streamlit",
        "Structure des tables Supabase",
        "Triggers et fonctions automatiques",

        "7. Annexes",
        "Glossaire",
        "Codes d’erreurs",
        "Procédures internes",
        "Contacts du comité"
    ]

    for line in sections:
        pdf.drawString(50, y, line)
        y -= 20
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = 750

    pdf.save()
    buffer.seek(0)
    return buffer

st.title("📘 Documentation du Club — Export PDF")

pdf_file = generate_pdf()

st.download_button(
    label="📄 Télécharger la documentation complète (PDF)",
    data=pdf_file,
    file_name="documentation_club.pdf",
    mime="application/pdf"
)
