import streamlit as st
from supabase_rest import supabase
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Activités Spéciales", page_icon="🎉")
st.title("🎉 Activités Spéciales")

# ---------------------------------------------------------
# Charger les activités (TA TABLE EXISTANTE)
# ---------------------------------------------------------
activites = (
    supabase.table("activites_speciales")
    .select("*")
    .order("date", desc=True)
    .execute()
    .data
)

# ---------------------------------------------------------
# État pour fiche activité
# ---------------------------------------------------------
if "act_id" not in st.session_state:
    st.session_state["act_id"] = None

# ---------------------------------------------------------
# Création d’une activité (dans TA TABLE)
# ---------------------------------------------------------
st.subheader("➕ Créer une activité")

nom = st.text_input("Nom de l’activité")
date_act = st.date_input("Date")
prix = st.number_input("Prix par personne (€)", min_value=0.0, step=1.0)
description = st.text_area("Description")

if st.button("Créer l’activité"):
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
            st.write(f"📅 {act['date']} — {act['prix_default']} €")

        with col3:
            if st.button("Gérer", key=f"gerer_{act['id']}"):
                st.session_state["act_id"] = act["id"]
                st.rerun()

else:
    st.info("Aucune activité.")

st.markdown("---")

# ---------------------------------------------------------
# FICHE ACTIVITÉ
# ---------------------------------------------------------
if st.session_state["act_id"] is not None:

    act_id = st.session_state["act_id"]

    act = (
        supabase.table("activites_speciales")
        .select("*")
        .eq("id", act_id)
        .execute()
        .data[0]
    )

    st.subheader(f"📄 Détail : {act['nom']}")

    st.write(f"**Date :** {act['date']}")
    st.write(f"**Prix par personne :** {act['prix_default']} €")
    st.write(f"**Description :** {act['description']}")

    st.markdown("---")

    # ---------------------------------------------------------
    # Inscription simple (TA TABLE EXISTANTE)
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

    if inscrits:
        total_general = sum(i["total"] for i in inscrits)

        for ins in inscrits:
            col1, col2, col3, col4 = st.columns([3, 3, 2, 2])

            with col1:
                st.write(f"{ins['nom']} {ins['prenom']}")

            with col2:
                st.write(f"{ins['nombre']} pers.")

            with col3:
                st.write(f"{ins['total']} €")

            with col4:
                if st.button("Supprimer", key=f"suppr_{ins['id']}"):
                    supabase.table("inscriptions_speciales").delete().eq("id", ins["id"]).execute()
                    st.rerun()

        st.markdown(f"### 💰 Total général : **{total_general} €**")

        # Export Excel
        df = pd.DataFrame(inscrits)
        st.download_button(
            "📥 Export Excel",
            df.to_csv(index=False).encode("utf-8"),
            "inscriptions.csv",
            "text/csv"
        )

        # Export PDF simple
        pdf_text = "\n".join([
            f"{i['nom']} {i['prenom']} — {i['nombre']} pers — {i['total']} €"
            for i in inscrits
        ])
        st.download_button(
            "📄 Export PDF",
            pdf_text.encode("utf-8"),
            "inscriptions.pdf",
            "application/pdf"
        )

    else:
        st.info("Aucun inscrit.")

    st.markdown("---")

    if st.button("⬅️ Fermer la fiche"):
        st.session_state["act_id"] = None
        st.rerun()
