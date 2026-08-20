import streamlit as st
from supabase import create_client
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Validation des présences", page_icon="🟢")

st.title("🟢 Validation des présences")

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
# Charger les séances actives
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
    st.info("Aucune séance active.")
    st.stop()

# ---------------------------------------------------------
# Détail d'une séance
# ---------------------------------------------------------
seance_detail = st.session_state.get("seance_detail", None)

if seance_detail:

    s = seance_detail
    cours = cours_dict.get(s["cours_id"], {})

    st.subheader("🔍 Détail de la séance")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"📅 **Date** : {s['date_seance']}")
        st.write(f"📝 **Note** : {s.get('note', 'Aucune note')}")

    with col2:
        st.write(f"🐾 **Cours** : {cours.get('nom', 'Cours inconnu')}")
        st.write(f"👤 **Instructeur** : {cours.get('instructeur', 'Non défini')}")
        st.write(f"📌 **Niveau** : {cours.get('niveau', 'Non défini')}")

    # ---------------------------------------------------------
    # Charger les préinscrits
    # ---------------------------------------------------------
    inscriptions = (
        supabase.table("cours_inscriptions")
        .select("*")
        .eq("seance_id", s["id"])
        .execute()
        .data
    )

    st.markdown("---")
    st.subheader("👥 Préinscrits")

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
    # PDF EXPORT
    # ---------------------------------------------------------
    st.markdown("---")
    st.subheader("📄 Export PDF")

    if st.button("📄 Télécharger la liste des préinscrits (PDF)"):

        # Regrouper par cours
        par_cours = {}
        for ins in inscriptions:
            cid = ins["cours_id"]
            par_cours.setdefault(cid, []).append(ins)

        # Création du PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Préinscrits – Séance du {s['date_seance']}", ln=True)
        pdf.ln(5)

        for cid, liste in par_cours.items():

            cours_info = cours_dict.get(cid, {})
            nom_cours = cours_info.get("nom", "Cours inconnu")

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, f"Cours : {nom_cours}", ln=True)

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

                pdf.cell(0, 6, f"- {membre_nom} — Chien : {chien_nom}", ln=True)

            pdf.ln(4)

        # Export PDF
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        st.download_button(
            label="📄 Télécharger le PDF",
            data=pdf_buffer,
            file_name=f"preinscrits_{s['date_seance']}.pdf",
            mime="application/pdf"
        )

    st.markdown("---")

# ---------------------------------------------------------
# LISTE DES SÉANCES ACTIVES
# ---------------------------------------------------------
st.subheader("📅 Séances actives")

for s in seances:

    cours = cours_dict.get(s["cours_id"], {})
    nom_cours = cours.get("nom", "Cours inconnu")

    col1, col2, col3 = st.columns([2, 2, 1])

    col1.write(f"📅 {s['date_seance']}")
    col2.write(f"🐾 {nom_cours}")

    if col3.button("Valider", key=f"voir_{s['id']}"):
        st.session_state["seance_detail"] = s

    st.markdown("---")
