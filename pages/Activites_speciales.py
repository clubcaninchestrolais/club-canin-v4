import streamlit as st
from supabase_rest import supabase
from datetime import datetime, date

st.set_page_config(page_title="Activités Spéciales", page_icon="🎉")
st.title("🎉 Activités Spéciales")

# ---------------------------------------------------------
# Charger les membres
# ---------------------------------------------------------
membres = (
    supabase.table("membres")
    .select("*")
    .order("nom")
    .execute()
    .data
)

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
# Charger les participants
# ---------------------------------------------------------
participants = (
    supabase.table("activites_participants")
    .select("*")
    .execute()
    .data
)

# ---------------------------------------------------------
# État pour fiche activité
# ---------------------------------------------------------
if "act_id" not in st.session_state:
    st.session_state["act_id"] = None

# ---------------------------------------------------------
# Création d’une activité
# ---------------------------------------------------------
st.subheader("➕ Créer une activité spéciale")

nom = st.text_input("Nom de l’activité")
description = st.text_area("Description")
date_act = st.date_input("Date")
lieu = st.text_input("Lieu")
prix = st.number_input("Prix (€)", min_value=0.0, step=1.0)
places = st.number_input("Nombre de places", min_value=0, step=1)

if st.button("Créer l’activité"):
    supabase.table("activites_speciales").insert({
        "nom": nom,
        "description": description,
        "date": date_act.isoformat(),
        "lieu": lieu,
        "prix": prix,
        "places": places
    }).execute()
    st.success("🎉 Activité créée avec succès.")
    st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Liste des activités
# ---------------------------------------------------------
st.subheader("📋 Liste des activités")

if activites:
    for act in activites:

        couleur = "#e6ffe6" if act["date"] >= date.today().isoformat() else "#ffcccc"

        col1, col2, col3, col4 = st.columns([3, 3, 3, 2])

        with col1:
            st.markdown(
                f"<div style='background:{couleur};padding:6px;border-radius:4px;'>"
                f"<b>{act['nom']}</b></div>",
                unsafe_allow_html=True
            )

        with col2:
            st.write(f"📅 {act['date']}")

        with col3:
            st.write(f"📍 {act['lieu']}")

        with col4:
            if st.button("Gérer", key=f"gerer_{act['id']}"):
                st.session_state["act_id"] = act["id"]
                st.rerun()

else:
    st.info("Aucune activité trouvée.")

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

    st.write(f"**Description :** {act['description']}")
    st.write(f"**Date :** {act['date']}")
    st.write(f"**Lieu :** {act['lieu']}")
    st.write(f"**Prix :** {act['prix']} €")
    st.write(f"**Places :** {act['places']}")

    st.markdown("---")

    # ---------------------------------------------------------
    # Inscription membre
    # ---------------------------------------------------------
    st.markdown("### ➕ Inscrire un membre")

    membre_options = [f"{m['nom']} {m['prenom']}" for m in membres]
    choix_membre = st.selectbox("Choisir un membre", membre_options)

    if st.button("Inscrire"):
        membre_sel = next(m for m in membres if f"{m['nom']} {m['prenom']}" == choix_membre)

        supabase.table("activites_participants").insert({
            "activite_id": act_id,
            "membre_id": membre_sel["id"],
            "present": False
        }).execute()

        st.success("Membre inscrit.")
        st.rerun()

    st.markdown("---")

    # ---------------------------------------------------------
    # Liste des participants
    # ---------------------------------------------------------
    st.markdown("### 👥 Participants")

    part_act = [p for p in participants if p["activite_id"] == act_id]

    if part_act:
        for p in part_act:

            membre = next(m for m in membres if m["id"] == p["membre_id"])

            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

            with col1:
                st.write(f"{membre['nom']} {membre['prenom']}")

            with col2:
                etat = "🟢 Présent" if p["present"] else "⚪ Absent"
                st.write(etat)

            with col3:
                if st.button("Présent", key=f"present_{p['id']}"):
                    supabase.table("activites_participants").update({
                        "present": True
                    }).eq("id", p["id"]).execute()
                    st.rerun()

            with col4:
                if st.button("Supprimer", key=f"suppr_{p['id']}"):
                    supabase.table("activites_participants").delete().eq("id", p["id"]).execute()
                    st.rerun()

    else:
        st.info("Aucun participant inscrit.")

    st.markdown("---")

    # ---------------------------------------------------------
    # Suppression activité
    # ---------------------------------------------------------
    if st.button("🗑️ Supprimer l’activité"):
        supabase.table("activites_speciales").delete().eq("id", act_id).execute()
        supabase.table("activites_participants").delete().eq("activite_id", act_id).execute()
        st.success("Activité supprimée.")
        st.session_state["act_id"] = None
        st.rerun()

    if st.button("⬅️ Fermer la fiche"):
        st.session_state["act_id"] = None
        st.rerun()
