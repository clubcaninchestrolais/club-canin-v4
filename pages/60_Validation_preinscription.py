import streamlit as st
from supabase_rest import supabase
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

st.set_page_config(page_title="Validation préinscription", page_icon="🐾")
st.title("🐾 Validation des préinscriptions extérieures")

# ---------------------------------------------------------
# 1. Charger les préinscriptions en attente
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
    st.info("Aucune préinscription en attente.")
    st.stop()

# ---------------------------------------------------------
# 2. Filtre
# ---------------------------------------------------------
filtre = st.text_input("🔍 Rechercher (nom, prénom, chien)")

if filtre:
    f = filtre.lower()
    preinscriptions = [
        p for p in preinscriptions
        if f in p["nom"].lower()
        or f in p["prenom"].lower()
        or f in p["chien_nom"].lower()
    ]

# ---------------------------------------------------------
# 3. Affichage en liste
# ---------------------------------------------------------
st.subheader("📋 Préinscriptions en attente")

for p in preinscriptions:

    # Charger la séance
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
        st.write(f"**{p['nom']} {p['prenom']}** — {p['chien_nom']}")

    with col2:
        st.write(f"{cours['nom']} — {seance['date_seance']}")

    with col3:
        if st.button("Valider", key=f"valider_{p['id']}"):

            # Créer le membre
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

            # Créer le chien
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

            # Inscription réelle
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

            # Inscription séance
            supabase.table("cours_seances_inscriptions").insert({
                "seance_id": p["seance_id"],
                "membre_id": membre_id,
                "chien_id": chien_id,
                "actif": True
            }).execute()

            # Mise à jour préinscription
            supabase.table("preinscriptions").update({
                "statut": "validee",
                "membre_id": membre_id,
                "chien_id": chien_id,
                "traitee": True,
                "acceptee": True,
                "type": "exterieur"
            }).eq("id", p["id"]).execute()

            st.success(f"Préinscription #{p['id']} validée.")
            st.experimental_rerun()

# ---------------------------------------------------------
# 4. PDF — Un PDF par séance regroupant tous les cours du jour
# ---------------------------------------------------------

st.subheader("📄 Générer le PDF de la journée")

# On prend la date de la première préinscription affichée
if preinscriptions:
    date_du_jour = seance["date_seance"]
else:
    date_du_jour = None

if st.button("Créer le PDF de la journée"):

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    # Titre principal
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, f"Séances du {date_du_jour}")

    y = 770

    # 1. Trouver toutes les séances du jour
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

        # Section du cours
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, f"Cours : {cours['nom']}")
        y -= 20

        pdf.setFont("Helvetica", 10)

        # Préinscriptions extérieures
        preinscriptions_seance = (
            supabase.table("preinscriptions")
            .select("*")
            .eq("seance_id", s["id"])
            .execute()
            .data
        )

        # Inscriptions membres
        inscriptions_membres = (
            supabase.table("cours_inscriptions")
            .select("*")
            .eq("seance_id", s["id"])
            .execute()
            .data
        )

        # Extérieurs
        for p in preinscriptions_seance:
            ligne = (
                f"{p['nom']} {p['prenom']} — "
                f"{p['chien_nom']} — extérieur — {p.get('source', 'portail')}"
            )
            pdf.drawString(70, y, ligne)
            y -= 20

            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = 800

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
                f"{membre['nom']} {membre['prenom']} — "
                f"{chien['nom']} — membre"
            )
            pdf.drawString(70, y, ligne)
            y -= 20

            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = 800

        # Séparateur
        y -= 10
        pdf.drawString(50, y, "---------------------------------------------")
        y -= 20

        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = 800

    pdf.save()
    buffer.seek(0)

    st.download_button(
        label="📥 Télécharger le PDF de la journée",
        data=buffer,
        file_name=f"seances_{date_du_jour}.pdf",
        mime="application/pdf"
    )

