import streamlit as st
from securite import securite_admin
securite_admin()

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral
from datetime import date, timedelta

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

chiens_dict = {c["id"]: c for c in chiens}

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

    # Regrouper les vaccins par chien
    vaccins_par_chien = {}
    for v in vaccins:
        cid = v["chien_id"]
        if cid not in vaccins_par_chien:
            vaccins_par_chien[cid] = []
        vaccins_par_chien[cid].append(v)

    # Affichage regroupé
    for chien_id, liste_vaccins in vaccins_par_chien.items():

        chien = chiens_dict.get(chien_id)
        if not chien:
            continue

        st.markdown(f"## 🐶 {chien['nom']}")

        # Dernier vaccin
        dernier = liste_vaccins[0]
        date_v = date.fromisoformat(dernier["date_vaccin"])

        # Date de fin de validité
        valid_until = dernier.get("valid_until")
        if valid_until:
            valid_until = date.fromisoformat(valid_until)
        else:
            valid_until = None

        # Statut
        today = date.today()

        if not valid_until:
            statut = "⚪ Validité inconnue"
        elif today > valid_until:
            statut = "🔴 Vaccin expiré"
        elif (valid_until - today).days < 30:
            statut = "🟠 Expire bientôt (< 30 jours)"
        else:
            statut = "🟢 À jour"

        st.write(f"**Statut :** {statut}")
        st.write(f"**Dernier vaccin :** {dernier['nom_vaccin']} — {dernier['date_vaccin']}")

        if valid_until:
            st.write(f"**Valide jusqu’au :** {valid_until}")
        else:
            st.write("**Valide jusqu’au :** Non défini")

        # Boutons utiles
        colA, colB = st.columns(2)

        with colA:
            if st.button("📄 Voir fiche chien", key=f"fiche_{chien_id}"):
                st.session_state["chien_id"] = chien_id
                st.switch_page("pages/22_Ajout_Chien.py")

        with colB:
            if st.button("➕ Ajouter un vaccin", key=f"addv_{chien_id}"):
                st.session_state["vaccin_chien_id"] = chien_id
                st.session_state["vaccin_mode"] = "ajout"
                st.session_state["vaccin_id"] = None
                st.rerun()

        # Liste des vaccins
        for v in liste_vaccins:
            with st.expander(f"{v['nom_vaccin']} — {v['date_vaccin']}"):
                st.write(f"💉 **Vaccin :** {v['nom_vaccin']}")
                st.write(f"📅 **Date :** {v['date_vaccin']}")
                st.write(f"📅 **Valide jusqu’au :** {v.get('valid_until', 'Non défini')}")
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

# Date de validité réelle (pas calcul automatique)
valid_until = st.date_input("Date de fin de validité")

remarques = st.text_area("Remarques (optionnel)")

if st.button("Ajouter le vaccin"):
    if not nom_vaccin:
        st.error("Le nom du vaccin est obligatoire.")
    else:
        supabase.table("vaccins").insert({
            "chien_id": chien_choisi["id"],
            "nom_vaccin": nom_vaccin,
            "date_vaccin": str(date_vaccin),
            "valid_until": str(valid_until),
            "remarques": remarques
        }).execute()

        st.success("Vaccin ajouté avec succès.")
        st.rerun()
