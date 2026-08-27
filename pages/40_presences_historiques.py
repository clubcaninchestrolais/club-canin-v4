import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase import create_client, Client

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Historique des présences", page_icon="📘")

st.title("📘 Historique des présences")

# ---------------------------------------------------------
# MODE 1 : Ouverture depuis la fiche membre
# ---------------------------------------------------------
if "historique_membre_id" in st.session_state:

    membre_id = st.session_state["historique_membre_id"]

    # Charger le membre
    membre = (
        supabase.table("membres")
        .select("*")
        .eq("id", membre_id)
        .execute()
        .data[0]
    )

    st.header(f"Historique de {membre['prenom']} {membre['nom']}")

    # Charger les présences
    presences = (
        supabase.table("cours_presences")
        .select("*")
        .eq("membre_id", membre_id)
        .order("date_presence", desc=True)
        .execute()
        .data
    )

    if not presences:
        st.info("Aucune présence enregistrée pour ce membre.")
        st.stop()

    st.markdown("---")
    st.subheader("Séances")

    # ---------------------------------------------------------
    # Affichage de l'historique
    # ---------------------------------------------------------
    for p in presences:

        # Récupérer la séance
        seance = (
            supabase.table("cours_seances")
            .select("*")
            .eq("id", p["seance_id"])
            .execute()
            .data
        )

        if not seance:
            st.warning(f"Séance inconnue (id {p['seance_id']})")
            continue

        seance = seance[0]
        date_seance = seance["date_seance"]
        cours_id = seance["cours_id"]

        # Récupérer le cours
        cours = (
            supabase.table("cours")
            .select("*")
            .eq("id", cours_id)
            .execute()
            .data
        )

        cours_nom = cours[0]["nom"] if cours else "Cours inconnu"

        # Récupérer le chien
        if p["chien_id"]:
            chien = (
                supabase.table("chiens")
                .select("*")
                .eq("id", p["chien_id"])
                .execute()
                .data
            )
            chien_nom = f"{chien[0]['nom']} ({chien[0]['race']})" if chien else "Chien inconnu"
        else:
            chien_nom = "Bénévole (pas de chien)"

        # Affichage
        st.write(f"📅 **{date_seance}** — *{cours_nom}*")
        st.write(f"🐶 **{chien_nom}**")
        st.write(f"Présent : {'✅ Oui' if p['present'] else '❌ Non'}")
        st.write("---")

    st.stop()

# ---------------------------------------------------------
# MODE 2 : Ouverture normale (depuis un menu)
# ---------------------------------------------------------

# Charger les membres
membres = (
    supabase.table("membres")
    .select("*")
    .order("nom")
    .execute()
    .data
)

if not membres:
    st.error("Aucun membre trouvé.")
    st.stop()

membre_labels = {f"{m['prenom']} {m['nom']}": m["id"] for m in membres}
membre_nom = st.selectbox("Sélectionnez un membre :", list(membre_labels.keys()))
membre_id = membre_labels[membre_nom]

# Charger les présences du membre
presences = (
    supabase.table("cours_presences")
    .select("*")
    .eq("membre_id", membre_id)
    .order("date_presence", desc=True)
    .execute()
    .data
)

if not presences:
    st.info("Aucune présence enregistrée pour ce membre.")
    st.stop()

st.markdown("---")
st.header("Historique des séances")

# Affichage
for p in presences:

    seance = (
        supabase.table("cours_seances")
        .select("*")
        .eq("id", p["seance_id"])
        .execute()
        .data
    )

    if not seance:
        st.warning(f"Séance inconnue (id {p['seance_id']})")
        continue

    seance = seance[0]
    date_seance = seance["date_seance"]
    cours_id = seance["cours_id"]

    cours = (
        supabase.table("cours")
        .select("*")
        .eq("id", cours_id)
        .execute()
        .data
    )

    cours_nom = cours[0]["nom"] if cours else "Cours inconnu"

    if p["chien_id"]:
        chien = (
            supabase.table("chiens")
            .select("*")
            .eq("id", p["chien_id"])
            .execute()
            .data
        )
        chien_nom = f"{chien[0]['nom']} ({chien[0]['race']})" if chien else "Chien inconnu"
    else:
        chien_nom = "Bénévole (pas de chien)"

    st.write(f"📅 **{date_seance}** — *{cours_nom}*")
    st.write(f"🐶 **{chien_nom}**")
    st.write(f"Présent : {'✅ Oui' if p['present'] else '❌ Non'}")
    st.write("---")
