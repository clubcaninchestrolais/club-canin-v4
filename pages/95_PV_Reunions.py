import streamlit as st
from securite import securite_admin
securite_admin()

from datetime import date
from supabase_rest import supabase

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

st.title("📄 PV des réunions")

st.write("Cette page permet de créer, consulter, télécharger et archiver les PV des réunions du comité.")

# ---------------------------------------------------------
# Création d'un PV
# ---------------------------------------------------------

st.subheader("Créer un nouveau PV")

titre = st.text_input("Titre du PV")
date_reunion = st.date_input("Date de la réunion", value=date.today())
contenu = st.text_area("Contenu du PV (compte rendu complet)")

if st.button("Enregistrer le PV"):
    data = {
        "titre": titre,
        "contenu": contenu,
        "date_reunion": str(date_reunion),
        "auteur": st.session_state.get("user_id", "admin")
    }
    supabase.table("pv_reunions").insert(data).execute()
    st.success("PV enregistré avec succès !")
    st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Liste des PV existants
# ---------------------------------------------------------

st.subheader("PV enregistrés")

pvs = (
    supabase.table("pv_reunions")
    .select("*")
    .order("date_reunion", desc=True)
    .execute()
    .data
)

if not pvs:
    st.info("Aucun PV enregistré pour le moment.")
else:
    for pv in pvs:
        with st.expander(f"📅 {pv['date_reunion']} — {pv['titre']}"):
            st.write(f"**Auteur :** {pv['auteur']}")
            st.write(f"**Créé le :** {pv['date_creation']}")
            st.markdown("---")
            st.write(pv["contenu"])

            # ---------------------------------------------------------
            # Génération PDF
            # ---------------------------------------------------------

            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=A4)
            pdf.setTitle(f"PV - {pv['date_reunion']}")

            width, height = A4
            y = height - 50

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(40, y, f"PV de réunion - {pv['date_reunion']}")
            y -= 30

            pdf.setFont("Helvetica", 12)
            pdf.drawString(40, y, f"Titre : {pv['titre']}")
            y -= 20
            pdf.drawString(40, y, f"Auteur : {pv['auteur']}")
            y -= 20
            pdf.drawString(40, y, f"Créé le : {pv['date_creation']}")
            y -= 40

            pdf.setFont("Helvetica", 11)

            for line in pv["contenu"].split("\n"):
                pdf.drawString(40, y, line)
                y -= 15
                if y < 40:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 11)
                    y = height - 50

            pdf.save()
            buffer.seek(0)

            st.download_button(
                label="📄 Télécharger le PV en PDF",
                data=buffer,
                file_name=f"PV_{pv['date_reunion']}.pdf",
                mime="application/pdf"
            )

            # ---------------------------------------------------------
            # Suppression du PV
            # ---------------------------------------------------------

            if st.button("🗑️ Supprimer ce PV", key=f"delete_{pv['id']}"):
                supabase.table("pv_reunions").delete().eq("id", pv["id"]).execute()
                st.rerun()
