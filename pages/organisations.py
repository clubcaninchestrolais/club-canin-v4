import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from io import BytesIO
from menu import hide_streamlit_menu, menu_lateral

st.set_page_config(page_title="Activités Spéciales", page_icon="🎉")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("🎉 Activités Spéciales")

# ---------------------------------------------------------
# Charger les activités
# ---------------------------------------------------------
activites = (
    supabase.table("activites_speciales")
    .select("*")
    .order("date", desc=True)
    .execute()
    .data
)

# ---------------------------------------------------------
# États internes
# ---------------------------------------------------------
if "act_id" not in st.session_state:
    st.session_state["act_id"] = None

if "show_fiche" not in st.session_state:
    st.session_state["show_fiche"] = False

# ---------------------------------------------------------
# Création d’une activité
# ---------------------------------------------------------
st.subheader("➕ Créer une activité")

nom = st.text_input("Nom de l'activité")
date_act = st.date_input("Date")
prix = float(st.number_input("Prix par personne (EUR)", min_value=0.0, step=1.0))
description = st.text_area("Description")

if st.button("Créer l'activité"):
    supabase.table("activites_speciales").insert({
        "nom": nom,
        "date": date_act.isoformat(),
        "prix_default": prix,
        "afficher_chien": False,
        "description": description
    }).execute()
    st.success("🎉 Activité créée.")
    st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Liste des activités
# ---------------------------------------------------------
st.subheader("📋 Liste des activités")

if activites:
    for act in activites:

        couleur = "#e6ffe6" if act["date"] >= datetime.now().date().isoformat() else "#ffcccc"

        col1, col2, col3 = st.columns([4, 3, 2])

        with col1:
            st.markdown(
                f"<div style='background:{couleur};padding:6px;border-radius:4px;'>"
                f"<b>{act['nom']}</b></div>",
                unsafe_allow_html=True
            )

        with col2:
            st.write(f"📅 {act['date']} — {act['prix_default']} EUR")

        with col3:
            if st.button("Gérer", key=f"gerer_{act['id']}"):
                st.session_state["act_id"] = act["id"]
                st.session_state["show_fiche"] = True
                st.rerun()

else:
    st.info("Aucune activité.")

st.markdown("---")

# ---------------------------------------------------------
# FICHE ACTIVITÉ
# ---------------------------------------------------------
if st.session_state["show_fiche"]:

    act_id = st.session_state["act_id"]

    act = (
        supabase.table("activites_speciales")
        .select("*")
        .eq("id", act_id)
        .execute()
        .data[0]
    )

    st.subheader(f"📄 Détail : {act['nom']}")

    # ---------------------------------------------------------
    # Modification de l’activité
    # ---------------------------------------------------------
    st.markdown("### ✏️ Modifier l'activité")

    with st.form("form_modif"):
        new_nom = st.text_input("Nom", act["nom"])
        new_date = st.date_input("Date", datetime.fromisoformat(act["date"]))
        new_prix = st.number_input("Prix par personne", min_value=0.0, value=float(act["prix_default"]))
        new_desc = st.text_area("Description", act["description"] or "")
        new_aff = st.checkbox("Afficher le choix du chien ?", act["afficher_chien"])

        submit_modif = st.form_submit_button("💾 Enregistrer")

        if submit_modif:
            supabase.table("activites_speciales").update({
                "nom": new_nom,
                "date": new_date.isoformat(),
                "prix_default": new_prix,
                "description": new_desc,
                "afficher_chien": new_aff
            }).eq("id", act_id).execute()

            st.success("Activité mise à jour.")
            st.rerun()

    st.markdown("---")

    # ---------------------------------------------------------
    # Inscription simple
    # ---------------------------------------------------------
    st.markdown("### ➕ Ajouter une inscription")

    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    nombre = st.number_input("Nombre de réservations", min_value=1, step=1)

    if st.button("Ajouter"):
        total = nombre * act["prix_default"]

        supabase.table("inscriptions_speciales").insert({
            "activite_id": act_id,
            "nom": nom,
            "prenom": prenom,
            "nombre": nombre,
            "total": total
        }).execute()

        st.success("Inscription ajoutée.")
        st.rerun()

    st.markdown("---")

    # ---------------------------------------------------------
    # Liste des inscrits
    # ---------------------------------------------------------
    st.markdown("### 👥 Liste des inscrits")

    inscrits = (
        supabase.table("inscriptions_speciales")
        .select("*")
        .eq("activite_id", act_id)
        .order("id")
        .execute()
        .data
    )

    # ---------------------------------------------------------
    # Fonction PDF
    # ---------------------------------------------------------
    def generate_pdf(inscrits, act):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.set_font("Arial", "B", 16)
        titre = f"Liste des inscrits - {act['nom']}"
        titre = titre.encode("latin-1", "replace").decode("latin-1")
        pdf.cell(0, 10, titre, ln=True)

        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, f"Date : {act['date']}", ln=True)
        pdf.cell(0, 8, f"Prix par personne : {act['prix_default']} EUR", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(60, 10, "Nom", 1)
        pdf.cell(60, 10, "Prénom", 1)
        pdf.cell(30, 10, "Nb", 1)
        pdf.cell(30, 10, "Total (EUR)", 1)
        pdf.ln()

        pdf.set_font("Arial", size=12)
        for i in inscrits:
            nom = i["nom"].encode("latin-1", "replace").decode("latin-1")
            prenom = i["prenom"].encode("latin-1", "replace").decode("latin-1")

            pdf.cell(60, 10, nom, 1)
            pdf.cell(60, 10, prenom, 1)
            pdf.cell(30, 10, str(i["nombre"]), 1)
            pdf.cell(30, 10, str(i["total"]), 1)
            pdf.ln()

        total_general = sum(i["total"] for i in inscrits)
        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Total général : {total_general} EUR", ln=True)

        buffer = BytesIO()
        pdf.output(buffer)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes

    # ---------------------------------------------------------
    # Affichage des inscrits
    # ---------------------------------------------------------
    if inscrits:
        total_general = sum(i["total"] for i in inscrits)

        for ins in inscrits:
            col1, col2, col3, col4 = st.columns([3, 3, 2, 2])

            with col1:
                st.write(f"{ins['nom']} {ins['prenom']}")

            with col2:
                st.write(f"{ins['nombre']} pers.")

            with col3:
                st.write(f"{ins['total']} EUR")

            with col4:
                if st.button("Supprimer", key=f"suppr_{ins['id']}"):
                    supabase.table("inscriptions_speciales").delete().eq("id", ins["id"]).execute()
                    st.rerun()

        st.markdown(f"### 💰 Total général : **{total_general} EUR**")

        df = pd.DataFrame(inscrits)
        st.download_button(
            "📥 Export Excel",
            df.to_csv(index=False).encode("utf-8"),
            "inscriptions.csv",
            "text/csv"
        )

        pdf_bytes = generate_pdf(inscrits, act)
        st.download_button(
            "📄 Télécharger PDF",
            pdf_bytes,
            file_name="inscriptions.pdf",
            mime="application/pdf"
        )

    else:
        st.info("Aucun inscrit.")

    st.markdown("---")

    if st.button("⬅️ Fermer la fiche"):
        st.session_state["show_fiche"] = False
        st.session_state["act_id"] = None
        st.rerun()

