import streamlit as st
from securite import securite_user
securite_user()

from supabase import create_client
from datetime import date

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("Validation des présences")

# ---------------------------------------------------------
# Charger les cours
# ---------------------------------------------------------
cours = (
    supabase.table("cours")
    .select("*")
    .order("nom")
    .execute()
    .data
)

cours_labels = {c["nom"]: c["id"] for c in cours}
cours_nom = st.selectbox("Filtrer par cours :", list(cours_labels.keys()))
cours_id = cours_labels[cours_nom]

# ---------------------------------------------------------
# Charger les séances du cours
# ---------------------------------------------------------
seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("cours_id", cours_id)
    .order("date_seance")
    .execute()
    .data
)

if not seances:
    st.info("Aucune séance pour ce cours.")
    st.stop()

seance_labels = {
    f"{s['nom_seance']} — {s['date_seance']}": s["id"]
    for s in seances
}

seance_nom = st.selectbox("Séance :", list(seance_labels.keys()))
seance_id = seance_labels[seance_nom]

# ---------------------------------------------------------
# Charger les inscriptions
# ---------------------------------------------------------
inscriptions = (
    supabase.table("cours_inscriptions")
    .select("*")
    .eq("seance_id", seance_id)
    .execute()
    .data
)

if not inscriptions:
    st.info("Aucun inscrit pour cette séance.")
    st.stop()

st.subheader("Liste des inscrits")

# ---------------------------------------------------------
# Boucle sur les inscrits
# ---------------------------------------------------------
for ins in inscriptions:

    # Charger membre
    membre = (
        supabase.table("membres")
        .select("*")
        .eq("id", ins["membre_id"])
        .execute()
        .data[0]
    )

    membre_nom = f"{membre['prenom']} {membre['nom']}"

    # Charger chien
    chien = None
    if ins["chien_id"]:
        chien = (
            supabase.table("chiens")
            .select("*")
            .eq("id", ins["chien_id"])
            .execute()
            .data[0]
        )

    chien_nom = chien["nom"] if chien else "(bénévole)"

    st.write(f"## {membre_nom} — 🐶 {chien_nom}")

    # ---------------------------------------------------------
    # Vérifier si présence déjà validée
    # ---------------------------------------------------------
    presence = (
        supabase.table("cours_presences")
        .select("*")
        .eq("membre_id", membre["id"])
        .eq("seance_id", seance_id)
        .execute()
        .data
    )

    if presence:
        st.success("Présence déjà validée")
        continue

    # ---------------------------------------------------------
    # AFFICHAGE DE LA SITUATION AVANT VALIDATION
    # ---------------------------------------------------------

    # Cotisation
    cot = (
        supabase.table("cotisations")
        .select("*")
        .eq("membre_id", membre["id"])
        .execute()
        .data
    )

    cotisation_ok = True

    if not cot:
        st.error("🟥 **Cotisation : Aucune cotisation trouvée**")
        cotisation_ok = False
    else:
        cot = cot[0]

        if cot["statut"] != "active":
            st.error("🟥 **Cotisation : NON ACTIVE**")
            cotisation_ok = False

        elif cot["date_expiration"] and cot["date_expiration"] < date.today().isoformat():
            st.error(f"🟥 **Cotisation expirée le {cot['date_expiration']}**")
            cotisation_ok = False

        else:
            st.success("🟩 Cotisation : OK")

    # Abonnement
    abo = (
        supabase.table("abonnements")
        .select("*")
        .eq("membre_id", membre["id"])
        .execute()
        .data
    )

    abonnement_ok = True

    if not abo:
        st.error("🟥 **Abonnement : Aucun abonnement trouvé**")
        abonnement_ok = False
    else:
        abo = abo[0]

        if not abo["actif"]:
            st.error("🟥 **Abonnement : NON ACTIF**")
            abonnement_ok = False

        elif abo["seances_restantes"] == 0:
            st.error("🟥 **Abonnement épuisé — 0 séance restante**")
            abonnement_ok = False

        elif abo["seances_restantes"] == -1:
            st.success("🟩 Abonnement : Illimité")

        else:
            st.success(f"🟩 Abonnement : {abo['seances_restantes']} séances restantes")

    # ---------------------------------------------------------
    # BOUTON DE VALIDATION
    # ---------------------------------------------------------
    if st.button(f"Valider présence — {membre_nom}"):

        # ---------------------------------------------------------
        # MESSAGE CLAIR SI PROBLÈME
        # ---------------------------------------------------------
        if not cotisation_ok or not abonnement_ok:
            st.error("""
🟥 **MEMBRE NON EN ORDRE — ACTION REQUISE**

Ce membre n'est pas en ordre d'abonnement ou de cotisation.

👉 **Le préposé doit :**
- vérifier avec le membre la raison du problème,
- régulariser l'abonnement ou la cotisation,
- informer le comité si nécessaire.

⚠️ La présence a été enregistrée, mais **le membre n'est pas en ordre**.
""")

        # ---------------------------------------------------------
        # ENREGISTRER LA PRÉSENCE
        # ---------------------------------------------------------
        supabase.table("cours_presences").insert({
            "membre_id": membre["id"],
            "chien_id": ins["chien_id"],
            "seance_id": seance_id,
            "present": True,
            "date_presence": date.today().isoformat()
        }).execute()

        # ---------------------------------------------------------
        # DÉCRÉMENTER L'ABONNEMENT SI OK
        # ---------------------------------------------------------
        if abo and abo["seances_restantes"] != -1 and abonnement_ok:
            reste = abo["seances_restantes"] - 1

            supabase.table("abonnements").update({
                "seances_restantes": reste,
                "actif": reste > 0
            }).eq("id", abo["id"]).execute()

        st.success("Présence validée")
