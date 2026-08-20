import streamlit as st
from supabase_client import supabase
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Validation préinscription", page_icon="📝")
st.title("📝 Validation des préinscriptions")

# ---------------------------------------------------------
# Charger les cours
# ---------------------------------------------------------
cours_table = supabase.table("cours").select("*").execute()

if cours_table.error:
    st.error(f"❌ Erreur chargement cours : {cours_table.error}")
    st.stop()

cours_list = cours_table.data or []
cours_dict = {c["id"]: c for c in cours_list}

# ---------------------------------------------------------
# Charger toutes les préinscriptions
# ---------------------------------------------------------
pre_table = supabase.table("preinscriptions").select("*").order("id", desc=True).execute()

if pre_table.error:
    st.error(f"❌ Erreur chargement préinscriptions : {pre_table.error}")
    st.stop()

preinscriptions = pre_table.data or []

if not preinscriptions:
    st.info("Aucune préinscription.")
    st.stop()

# ---------------------------------------------------------
# PDF
# ---------------------------------------------------------
st.subheader("📄 Export PDF — Préinscrits par cours")

if st.button("📄 Télécharger la liste des préinscrits (PDF)"):

    cours_dict_pdf = {}

    for pre in preinscriptions:
        cours_id = pre.get("cours_id")
        cours_type = cours_dict.get(cours_id, {}).get("nom", "Cours inconnu")
        cours_dict_pdf.setdefault(cours_type, []).append(pre)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Liste des preinscrits par cours", ln=True)
    pdf.ln(5)

    for cours_type, liste in cours_dict_pdf.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"Cours : {cours_type}", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.ln(2)

        for pre in liste:
            membre_nom = f"{pre.get('prenom','')} {pre.get('nom','')}"
            chien_nom = pre.get("chien_nom", "Chien")
            date_seance = pre.get("date_seance", "")
            heure = pre.get("heure_debut", "")
            pdf.cell(0, 6, f"- {membre_nom} - Chien : {chien_nom} - {date_seance} {heure}", ln=True)

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
# Affichage compact avec couleur
# ---------------------------------------------------------
st.subheader("📋 Préinscriptions (traitées + en attente)")

for pre in preinscriptions:

    nom_complet = f"{pre.get('prenom','')} {pre.get('nom','')}"
    chien = pre.get("chien_nom", "")

    cours_id = pre.get("cours_id")
    cours_type = cours_dict.get(cours_id, {}).get("nom", "Cours inconnu")

    date_seance = pre.get("date_seance", "")
    heure = pre.get("heure_debut", "")

    # Couleur selon état
    if pre.get("traitee"):
        bg = "background-color: #d4f8d4;"   # vert clair
    else:
        bg = "background-color: #f8e6d4;"   # orange clair

    st.markdown(
        f"""
        <div style="{bg}; padding:10px; border-radius:8px; margin-bottom:8px;">
            <b>👤 {nom_complet}</b><br>
            🐶 {chien}<br>
            📘 {cours_type}<br>
            📅 {date_seance} — ⏰ {heure}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Bouton seulement si NON traité
    if not pre.get("traitee"):
        if st.button("Valider", key=f"val_{pre['id']}"):
            st.session_state["pre_id"] = pre["id"]
            st.session_state["go_validation"] = True
            st.rerun()
    else:
        st.write("✔ Déjà validé")

st.markdown("---")

# ---------------------------------------------------------
# Validation d'une préinscription
# ---------------------------------------------------------
if st.session_state.get("go_validation", False):

    st.session_state["go_validation"] = False
    pre_id = st.session_state["pre_id"]

    pre_data = supabase.table("preinscriptions").select("*").eq("id", pre_id).execute()

    if pre_data.error or not pre_data.data:
        st.error("❌ Impossible de charger la préinscription.")
        st.stop()

    pre = pre_data.data[0]

    cours_id = pre.get("cours_id")
    cours_type = cours_dict.get(cours_id, {}).get("nom", "Cours inconnu")

    st.subheader("🔍 Validation de la préinscription")

    st.write(f"👤 **{pre.get('prenom', '')} {pre.get('nom', '')}**")
    st.write(f"📧 {pre.get('email', 'Non spécifié')}")
    st.write(f"📱 {pre.get('telephone', 'Non spécifié')}")
    st.write(f"🐶 **Chien :** {pre.get('chien_nom', 'Non spécifié')}")
    st.write(f"📘 **Cours :** {cours_type}")
    st.write(f"📅 **Date :** {pre.get('date_seance', '')}")
    st.write(f"⏰ **Heure :** {pre.get('heure_debut', '')}")

    st.markdown("---")

    if st.button("Créer le membre"):

        # 1) Création du membre
        membre_insert = {
            "nom": pre.get("nom", ""),
            "prenom": pre.get("prenom", ""),
            "email": pre.get("email", ""),
            "telephone": pre.get("telephone", ""),
            "statut": "exterieur",
            "actif": False
        }

        membre_result = supabase.table("membres").insert(membre_insert).execute()

        if membre_result.error:
            st.error(f"❌ Erreur création membre : {membre_result.error}")
            st.stop()

        membre_id = membre_result.data[0]["id"]

        # 2) Création du chien
        chien_insert = {
            "nom": pre.get("chien_nom", "Chien"),
            "membre_id": membre_id
        }

        chien_result = supabase.table("chiens").insert(chien_insert).execute()

        if chien_result.error:
            st.error(f"❌ Erreur création chien : {chien_result.error}")
            st.stop()

        # 3) Marquer comme traitée
        update_result = supabase.table("preinscriptions").update({"traitee": True}).eq("id", pre_id).execute()

        if update_result.error:
            st.error(f"❌ Erreur mise à jour préinscription : {update_result.error}")
            st.stop()

        st.success("🎉 Membre et chien créés avec succès.")
        st.rerun()


