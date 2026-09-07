import streamlit as st
from securite import securite_admin
securite_admin()

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral
from datetime import date

hide_streamlit_menu()
menu_lateral()

st.title("💉 Gestion des vaccins des chiens")

# ---------------------------------------------------------
# FILTRES EN HAUT DE PAGE
# ---------------------------------------------------------

filtre_nom = st.text_input("Filtrer par nom du chien")

filtre_statut = st.selectbox(
    "Filtrer par statut",
    ["Tous", "À jour", "Expire bientôt", "Expirés", "Validité inconnue"]
)

st.markdown("---")

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

        # --- FILTRE PAR NOM ---
        if filtre_nom and filtre_nom.lower() not in chien["nom"].lower():
            continue

        # Dernier vaccin
        dernier = liste_vaccins[0]
        date_v = date.fromisoformat(dernier["date_vaccin"])

        # Date de validité
        valid_until = dernier.get("valid_until")
        if valid_until:
            valid_until = date.fromisoformat(valid_until)
        else:
            valid_until = None

        # Statut
        today = date.today()

        if not valid_until:
            statut = "Validité inconnue"
            statut_code = "inconnu"
        elif today > valid_until:
            statut = "Vaccin expiré"
            statut_code = "expire"
        elif (valid_until - today).days < 30:
            statut = "Expire bientôt"
            statut_code = "bientot"
        else:
            statut = "À jour"
            statut_code = "ajour"

        # --- FILTRE STATUT ---
        if filtre_statut == "À jour" and statut_code != "ajour":
            continue
        if filtre_statut == "Expire bientôt" and statut_code != "bientot":
            continue
        if filtre_statut == "Expirés" and statut_code != "expire":
            continue
        if filtre_statut == "Validité inconnue" and statut_code != "inconnu":
            continue

        # ---------------------------------------------------------
        # CODE COULEUR
        # ---------------------------------------------------------
        if statut_code == "expire":
            couleur = "#ffcccc"   # rouge clair
        elif statut_code == "bientot":
            couleur = "#ffe6cc"   # orange clair
        elif statut_code == "ajour":
            couleur = "#e6ffe6"   # vert clair
        else:
            couleur = "#f2f2f2"   # gris clair

        # Encadré coloré
        st.markdown(
            f"""
            <div style="padding: 12px; border-radius: 8px; background-color: {couleur};">
                <b>{chien['nom']}</b><br>
                Statut : {statut}<br>
                Dernier vaccin : {dernier['nom_vaccin']} — {dernier['date_vaccin']}<br>
                Valide jusqu’au : {valid_until if valid_until else "Non défini"}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------------------------------------------------------
        # BOUTONS DIRECTS
        # ---------------------------------------------------------

        col1, col2 = st.columns(2)

        # --- BOUTON MODIFIER ---
        with col1:
            if st.button("✏️ Modifier le dernier vaccin", key=f"edit_last_{chien_id}"):
                st.session_state["vaccin_id"] = dernier["id"]
                st.switch_page("pages/modifier_vaccin.py")

        # --- BOUTON AJOUTER ---
        with col2:
            if st.button("➕ Ajouter un vaccin", key=f"addv_{chien_id}"):
                st.session_state["vaccin_chien_id"] = chien_id
                st.session_state["vaccin_mode"] = "ajout"
                st.session_state["vaccin_id"] = None
                st.rerun()

        # ---------------------------------------------------------
        # HISTORIQUE DES VACCINS
        # ---------------------------------------------------------

        with st.expander("Historique des vaccins"):
            for v in liste_vaccins:
                st.write(f"💉 {v['nom_vaccin']} — {v['date_vaccin']} — Valide jusqu’au : {v.get('valid_until', 'Non défini')}")

                colA, colB = st.columns(2)

                with colA:
                    if st.button("✏️ Modifier", key=f"edit_{v['id']}"):
                        st.session_state["vaccin_id"] = v["id"]
                        st.switch_page("pages/modifier_vaccin.py")

                with colB:
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
