import streamlit as st
from securite import securite_admin
securite_admin()

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

hide_streamlit_menu()
menu_lateral()

st.title("💉 Gestion des vaccins des chiens")

# ---------------------------------------------------------
# Charger les chiens
# ---------------------------------------------------------

chiens = (
    supabase.table("chiens")
    .select("*")
    .order("nom")
    .execute()
    .data
)

# Dictionnaire id → nom du chien
chiens_dict = {c["id"]: c["nom"] for c in chiens}

# ---------------------------------------------------------
# Charger les vaccins
# ---------------------------------------------------------

vaccins = (
    supabase.table("vaccins")
    .select("*")
    .order("date_vaccin", desc=True)
    .execute()
    .data
)

st.subheader("Vaccins enregistrés")

if not vaccins:
    st.info("Aucun vaccin enregistré pour le moment.")
else:
    for v in vaccins:
        chien_nom = chiens_dict.get(v["chien_id"], "Chien inconnu")

        with st.expander(f"{chien_nom} — {v['nom_vaccin']} ({v['date_vaccin']})"):
            st.write(f"🐶 **Chien :** {chien_nom}")
            st.write(f"💉 **Vaccin :** {v['nom_vaccin']}")
            st.write(f"📅 **Date :** {v['date_vaccin']}")
            st.write(f"📝 **Remarques :** {v['remarques']}")
            st.write(f"🕒 **Créé le :** {v['created_at']}")

            if st.button("🗑️ Supprimer", key=f"delete_{v['id']}"):
                supabase.table("vaccins").delete().eq("id", v["id"]).execute()
                st.success("Vaccin supprimé.")
                st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Ajouter un vaccin
# ---------------------------------------------------------

st.subheader("Ajouter un vaccin")

if not chiens:
    st.warning("Aucun chien enregistré. Impossible d'ajouter un vaccin.")
    st.stop()

chien_choisi = st.selectbox(
    "Sélectionner le chien",
    options=chiens,
    format_func=lambda c: f"{c['nom']}"
)

nom_vaccin = st.text_input("Nom du vaccin")
date_vaccin = st.date_input("Date du vaccin")
remarques = st.text_area("Remarques (optionnel)")

if st.button("Ajouter le vaccin"):
    if not nom_vaccin:
        st.error("Le nom du vaccin est obligatoire.")
    else:
        supabase.table("vaccins").insert({
            "chien_id": chien_choisi["id"],
            "nom_vaccin": nom_vaccin,
            "date_vaccin": str(date_vaccin),
            "remarques": remarques
        }).execute()

        st.success("Vaccin ajouté avec succès.")
        st.rerun()
