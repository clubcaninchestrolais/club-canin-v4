import streamlit as st
from securite import securite_admin
securite_admin()

from datetime import datetime
from supabase_rest import supabase

st.title("📢 Gestion des notifications internes")

st.write("Cette page permet à l’administrateur de créer et gérer les notifications visibles par les utilisateurs du club.")

# ---------------------------------------------------------
# Formulaire de création
# ---------------------------------------------------------

st.subheader("Créer une nouvelle notification")

titre = st.text_input("Titre")
message = st.text_area("Message")
role = st.selectbox("Destinataires", ["all", "user", "admin"])
actif = st.checkbox("Notification active", value=True)

if st.button("Créer la notification"):
    data = {
        "titre": titre,
        "message": message,
        "role": role,
        "actif": actif,
        "date": datetime.now().isoformat()
    }
    supabase.table("notifications").insert(data).execute()
    st.success("Notification créée avec succès !")

st.markdown("---")

# ---------------------------------------------------------
# Liste des notifications existantes
# ---------------------------------------------------------

st.subheader("Notifications existantes")

notifs = supabase.table("notifications").select("*").order("id", desc=True).execute().data

if notifs:
    for n in notifs:
        st.markdown(f"### 📌 {n['titre']}")
        st.write(n["message"])
        st.write(f"👥 Destinataires : **{n['role']}**")
        st.write(f"📅 Créée le : {n['date']}")
        st.write(f"🔔 Active : {'Oui' if n['actif'] else 'Non'}")

        # Bouton pour activer/désactiver
        new_state = not n["actif"]
        if st.button(f"{'Désactiver' if n['actif'] else 'Activer'}", key=f"toggle_{n['id']}"):
            supabase.table("notifications").update({"actif": new_state}).eq("id", n["id"]).execute()
            st.experimental_rerun()

        # Bouton pour supprimer
        if st.button("🗑️ Supprimer", key=f"delete_{n['id']}"):
            supabase.table("notifications").delete().eq("id", n["id"]).execute()
            st.rerun()

        st.markdown("---")
else:
    st.info("Aucune notification pour le moment.")
