import streamlit as st
from securite import securite_admin
securite_admin()

from datetime import date
from supabase_rest import supabase

from fpdf import FPDF
import io

st.title("📄 PV des réunions")

st.write("Créer, consulter, télécharger et archiver les PV des réunions du comité.")

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
            # Génération PDF via FPDF
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
            pdf.ln(25)
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

            buffer = io.BytesIO()
            pdf.output(buffer)
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
