import streamlit as st
from supabase import create_client
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Validation des presences", page_icon="🟢")

st.title("🟢 Validation des presences")

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# ---------------------------------------------------------
# Charger les cours
# ---------------------------------------------------------
cours_dict = {
    c["id"]: c
    for c in supabase.table("cours").select("*").execute().data
}

# ---------------------------------------------------------
# Charger les seances actives
# ---------------------------------------------------------
seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("actif", True)
    .order("date_seance", desc=False)
    .execute()
    .data
)

if not seances:
    st.info("Aucune seance active.")
    st.stop()

# ---------------------------------------------------------
# Detail d'une seance
# ---------------------------------------------------------
seance_detail = st.session_state.get("seance_detail", None)

if seance_detail:

    s = seance_detail
    cours = cours_dict.get(s["cours_id"], {})

    st.subheader("🔍 Detail de la seance")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"📅 **Date** : {s['date_seance']}")
        st.write(f"📝 **Note** : {s.get('note', 'Aucune note')}")

    with col2:
        st.write(f"🐾 **Cours** : {cours.get('nom', 'Cours inconnu')}")
        st.write(f"👤 **Instructeur** : {cours.get('instructeur', 'Non defini')}")
        st.write(f"📌 **Niveau** : {cours.get('niveau', 'Non defini')}")

    # ---------------------------------------------------------
    # Charger les preinscrits
    # ---------------------------------------------------------
    inscriptions = (
        supabase.table("cours_inscriptions")
        .select("*")
        .eq("seance_id", s["id"])
        .execute()
        .data
    )

    st.markdown("---")
    st.subheader("👥 Preinscrits")

    for ins in inscriptions:
        membre = (
            supabase.table("membres")
            .select("*")
            .eq("id", ins["membre_id"])
            .execute()
            .data
        )
        chien = (
            supabase.table("chiens")
            .select("*")
            .eq("id", ins["chien_id"])
            .execute()
            .data
        )

        membre_nom = (
            f"{membre[0]['prenom']} {membre[0]['nom']}"
            if membre else "Membre inconnu"
        )
        chien_nom = chien[0]["nom"] if chien else "Chien inconnu"

        st.write(f"- **{membre_nom}** — 🐶 {chien_nom}")

    # ---------------------------------------------------------
    # PDF EXPORT (sans accents)
    # ---------------------------------------------------------
    st.markdown("---")
    st.subheader("📄 Export PDF")

    if st.button("📄 Telecharger la liste des preinscrits (PDF)"):

        # Regrouper par cours
        par_cours = {}
        for ins in inscriptions:
            cid = ins["cours_id"]
            par_cours.setdefault(cid, []).append(ins)

        # Creation du PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Titre SANS accents
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Preinscrits - Seance du {s['date_seance']}", ln=True)
        pdf.ln(5)

        # Contenu par cours
        for cid, liste in par_cours.items():

            cours_info = cours_dict.get(cid, {})
            nom_cours = cours_info.get("nom", "Cours inconnu")

            # Enlever accents du nom du cours
            nom_cours_sans_accents = nom_cours.encode("ascii", "ignore").decode()

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, f"Cours : {nom_cours_sans_accents}", ln=True)

            pdf.set_font("Arial", size=11)

            for ins in liste:
                membre = (
                    supabase.table("membres")
                    .select("*")
                    .eq("id", ins["membre_id"])
                    .execute()
                    .data
                )
                chien = (
                    supabase.table("chiens")
                    .select("*")
                    .eq("id", ins["chien_id"])
                    .execute()
                    .data
                )

                membre_nom = (
                    f"{membre[0]['prenom']} {membre[0]['nom']}"
                    if membre else "Membre inconnu"
                )
                chien_nom = chien[0]["nom"] if chien else "Chien inconnu"

                # Enlever accents
                membre_nom = membre_nom.encode("ascii", "ignore").decode()
                chien_nom = chien_nom.encode("ascii", "ignore").decode()

                pdf.cell(0, 6, f"- {membre_nom} - Chien : {chien_nom}", ln=True)

            pdf.ln(4)

        # Export PDF
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        st.download_button(
            label="📄 Telecharger le PDF",
            data=pdf_buffer,
            file_name=f"preinscrits_{s['date_seance']}.pdf",
            mime="application/pdf"
        )

    st.markdown("---")

# ---------------------------------------------------------
# LISTE DES SEANCES ACTIVES
# ---------------------------------------------------------
st.subheader("📅 Seances actives")

for s in seances:

    cours = cours_dict.get(s["cours_id"], {})
    nom_cours = cours.get("nom", "Cours inconnu")

    col1, col2, col3 = st.columns([2, 2, 1])

    col1.write(f"📅 {s['date_seance']}")
    col2.write(f"🐾 {nom_cours}")

    if col3.button("Valider", key=f"voir_{s['id']}"):
        st.session_state["seance_detail"] = s

    st.markdown("---")
