import streamlit as st
from supabase_rest import supabase
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Validation preinscription", page_icon="🐾")
st.title("🐾 Validation des preinscriptions exterieures")

# ---------------------------------------------------------
# 1. Charger les preinscriptions en attente
# ---------------------------------------------------------
preinscriptions = (
    supabase.table("preinscriptions")
    .select("*")
    .eq("statut", "En attente")
    .order("date_preinscription")
    .execute()
    .data
)

if not preinscriptions:
    st.info("Aucune preinscription en attente.")
    st.stop()

# ---------------------------------------------------------
# 2. Filtre
# ---------------------------------------------------------
filtre = st.text_input("🔍 Rechercher (nom, prenom, chien)")

if filtre:
    f = filtre.lower()
    preinscriptions = [
        p for p in preinscriptions
        if f in p["nom"].lower()
        or f in p["prenom"].lower()
        or f in p["chien_nom"].lower()
    ]

# ---------------------------------------------------------
# 3. Affichage en liste + validation
# ---------------------------------------------------------
st.subheader("📋 Preinscriptions en attente")

for p in preinscriptions:

    # Charger la seance
    seance_data = (
        supabase.table("cours_seances")
        .select("*")
        .eq("id", p["seance_id"])
        .execute()
        .data
    )
    if not seance_data:
        continue

    seance = seance_data[0]

    # Charger le cours
    cours_data = (
        supabase.table("cours")
        .select("*")
        .eq("id", seance["cours_id"])
        .execute()
        .data
    )
    cours = cours_data[0]

    col1, col2, col3 = st.columns([4, 3, 2])

    with col1:
        st.write(f"**{p['nom']} {p['prenom']}** - {p['chien_nom']}")

    with col2:
        st.write(f"{cours['nom']} - {seance['date_seance']}")

    with col3:
        if st.button("Valider", key=f"valider_{p['id']}"):

            # Creer le membre
            membre = (
                supabase.table("membres")
                .insert({
                    "nom": p["nom"],
                    "prenom": p["prenom"],
                    "email": p["email"],
                    "telephone": p["telephone"],
                    "statut": "non_membre",
                    "actif": False
                })
                .execute()
                .data[0]
            )
            membre_id = membre["id"]

            # Creer le chien
            chien = (
                supabase.table("chiens")
                .insert({
                    "nom": p["chien_nom"],
                    "race": p["chien_race"],
                    "membre_id": membre_id,
                    "actif": True
                })
                .execute()
                .data[0]
            )
            chien_id = chien["id"]

            # Inscription reelle
            supabase.table("cours_inscriptions").insert({
                "membre_id": membre_id,
                "chien_id": chien_id,
                "cours_id": cours["id"],
                "seance_id": p["seance_id"],
                "date_seance": seance["date_seance"],
                "type": "exterieur",
                "source": "preinscription",
                "actif": True
            }).execute()

            # Inscription seance
            supabase.table("cours_seances_inscriptions").insert({
                "seance_id": p["seance_id"],
                "membre_id": membre_id,
                "chien_id": chien_id,
                "actif": True
            }).execute()

            # Mise a jour preinscription
            supabase.table("preinscriptions").update({
                "statut": "validee",
                "membre_id": membre_id,
                "chien_id": chien_id,
                "traitee": True,
                "acceptee": True,
                "type": "exterieur"
            }).eq("id", p["id"]).execute()

            st.success(f"Preinscription #{p['id']} validee.")
            st.experimental_rerun()

# ---------------------------------------------------------
# 4. PDF – un PDF pour la journee (toutes les seances / cours)
# ---------------------------------------------------------
st.subheader("📄 Generer le PDF de la journee")

if preinscriptions:
    date_du_jour = seance["date_seance"]
else:
    date_du_jour = None

if date_du_jour and st.button("Creer le PDF de la journee"):

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "", 16)
    pdf.cell(0, 10, f"Seances du {date_du_jour}", ln=True)

    # 1. Toutes les seances de cette date
    toutes_seances = (
        supabase.table("cours_seances")
        .select("*")
        .eq("date_seance", date_du_jour)
        .execute()
        .data
    )

    for s in toutes_seances:

        # Charger le cours
        cours_data = (
            supabase.table("cours")
            .select("*")
            .eq("id", s["cours_id"])
            .execute()
            .data
        )
        cours = cours_data[0]

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Cours : {cours['nom']}", ln=True)

        pdf.set_font("Arial", "", 10)

        # Preinscriptions exterieures
        preinscriptions_seance = (
            supabase.table("preinscriptions")
            .select("*")
            .eq("seance_id", s["id"])
            .execute()
            .data
        )

        # Membres inscrits
        inscriptions_membres = (
            supabase.table("cours_inscriptions")
            .select("*")
            .eq("seance_id", s["id"])
            .execute()
            .data
        )

        # Exterieurs
        for p in preinscriptions_seance:
            ligne = (
                f"{p['nom']} {p['prenom']} - "
                f"{p['chien_nom']} - exterieur - {p.get('source', 'portail')}"
            )
            pdf.cell(0, 8, ligne, ln=True)

        # Membres
        for ins in inscriptions_membres:

            membre = (
                supabase.table("membres")
                .select("*")
                .eq("id", ins["membre_id"])
                .execute()
                .data[0]
            )

            chien = (
                supabase.table("chiens")
                .select("*")
                .eq("id", ins["chien_id"])
                .execute()
                .data[0]
            )

            ligne = (
                f"{membre['nom']} {membre['prenom']} - "
                f"{chien['nom']} - membre"
            )
            pdf.cell(0, 8, ligne, ln=True)

        pdf.ln(5)
        pdf.cell(0, 5, "---------------------------------------------", ln=True)
        pdf.ln(5)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    st.download_button(
        label="📥 Telecharger le PDF de la journee",
        data=buffer,
        file_name=f"seances_{date_du_jour}.pdf",
        mime="application/pdf"
    )

