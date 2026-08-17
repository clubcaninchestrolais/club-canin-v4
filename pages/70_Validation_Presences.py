import streamlit as st
from supabase_rest import supabase

st.set_page_config(page_title="Validation des présences", page_icon="📝")
st.title("📝 Validation des présences")

# ---------------------------------------------------------
# Charger les séances disponibles
# ---------------------------------------------------------
seances = (
    supabase.table("cours_seances")
    .select("*")
    .order("date_seance")
    .execute()
    .data
)

if not seances:
    st.error("Aucune séance disponible.")
    st.stop()

# Choix de la séance
choix = st.selectbox(
    "Séance",
    options=seances,
    format_func=lambda s: f"{s['date_seance']} — cours {s['cours_id']} ({s['heure_debut']})"
)

cours_id_selectionne = choix["cours_id"]
date_seance_selectionnee = choix["date_seance"]

st.markdown("---")

# ---------------------------------------------------------
# Charger les inscrits pour cette séance
# ---------------------------------------------------------
inscrits = (
    supabase.table("cours_presences")
    .select("id, membre_id, chien_id, statut")
    .eq("cours_id", cours_id_selectionne)
    .eq("date_presence", date_seance_selectionnee)
    .execute()
    .data
)

if not inscrits:
    st.info("Aucun inscrit pour cette séance.")
    st.stop()

st.success(f"{len(inscrits)} inscrit(s) trouvé(s).")

# ---------------------------------------------------------
# Affichage des inscrits + validation
# ---------------------------------------------------------
for i in inscrits:
    st.markdown("---")

    # Récupérer infos membre
    membre = (
        supabase.table("membres")
        .select("prenom, nom")
        .eq("id", i["membre_id"])
        .execute()
        .data
    )[0]

    st.subheader(f"👤 {membre['prenom']} {membre['nom']}")

    # Récupérer infos chien
    if i["chien_id"]:
        chien = (
            supabase.table("chiens")
            .select("nom")
            .eq("id", i["chien_id"])
            .execute()
            .data
        )[0]
        st.write(f"🐶 Chien : **{chien['nom']}**")

    # Afficher compteur abonnement
    abo = (
        supabase.table("abonnements")
        .select("id, seances_total, seances_restantes")
        .eq("id_membre", i["membre_id"])
        .order("id", desc=True)
        .execute()
        .data
    )[0]

    st.write(f"🎫 Séances restantes : **{abo['seances_restantes']}** / {abo['seances_total']}")

    # Statut actuel
    statut = i.get("statut", "absent")
    st.write(f"📌 Statut actuel : **{statut}**")

    col1, col2 = st.columns(2)

    # Bouton valider présence
    if col1.button(f"✔ Présent — {i['id']}", key=f"present_{i['id']}"):
        supabase.table("cours_presences").update({
            "statut": "present"
        }).eq("id", i["id"]).execute()

        # Décrémentation ici
        if abo["seances_total"] != -1 and abo["seances_restantes"] > 0:
            supabase.table("abonnements").update({
                "seances_restantes": abo["seances_restantes"] - 1
            }).eq("id", abo["id"]).execute()

        st.success("Présence validée et séance consommée.")
        st.rerun()

    # Bouton marquer absent
    if col2.button(f"❌ Absent — {i['id']}", key=f"absent_{i['id']}"):
        supabase.table("cours_presences").update({
            "statut": "absent"
        }).eq("id", i["id"]).execute()

        st.warning("Présence marquée comme absente (aucune séance consommée).")
        st.rerun()
