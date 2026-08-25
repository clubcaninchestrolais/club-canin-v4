import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase
from datetime import datetime
from menu import hide_streamlit_menu, menu_lateral   # <-- AJOUT

st.set_page_config(page_title="Présence du jour", page_icon="📋")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()   # <-- AJOUT

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()          # <-- AJOUT

st.title("📋 Présence du jour")

# ---------------------------------------------------------
# Charger les séances (nouveau modèle sans heure_debut / heure_fin)
# ---------------------------------------------------------
seances = (
    supabase.table("cours_seances")
    .select("id, cours_id, date_seance")
    .order("date_seance")
    .execute()
    .data
)

if not seances:
    st.error("Aucune séance trouvée.")
    st.stop()

# Charger les cours pour afficher le nom
cours = supabase.table("cours").select("*").execute().data
cours_dict = {c["id"]: c["nom"] for c in cours}

# Construire labels complets
seance_labels = {}
for s in seances:
    cours_nom = cours_dict.get(s["cours_id"], "Cours inconnu")
    label = f"{s['date_seance']} — cours {s['cours_id']} — {cours_nom}"
    seance_labels[label] = s["id"]

# IMPORTANT : key= pour forcer Streamlit à mettre à jour la sélection
selection = st.selectbox("Séance :", list(seance_labels.keys()), key="select_seance")
seance_id = seance_labels[selection]

# Charger la séance sélectionnée
seance = (
    supabase.table("cours_seances")
    .select("*")
    .eq("id", seance_id)
    .execute()
    .data[0]
)

st.subheader(f"Participants pour la séance du {seance['date_seance']} — cours {seance['cours_id']}")

# ---------------------------------------------------------
# Charger les présences de cette séance
# ---------------------------------------------------------
presences = (
    supabase.table("cours_presences")
    .select("*")
    .eq("seance_id", seance_id)
    .execute()
    .data
)

if not presences:
    st.info("Aucun participant pour cette séance.")
    st.stop()

# ---------------------------------------------------------
# Affichage des participants
# ---------------------------------------------------------
for p in presences:

    membre_id = p["membre_id"]
    chien_id = p["chien_id"]

    # Charger membre (membre ou extérieur)
    membre = (
        supabase.table("membres")
        .select("*")
        .eq("id", membre_id)
        .execute()
        .data
    )

    if membre:
        membre = membre[0]
        nom_affiche = f"{membre['prenom']} {membre['nom']} (Membre)"
    else:
        candidat = (
            supabase.table("candidats")
            .select("*")
            .eq("id", membre_id)
            .execute()
            .data
        )
        if candidat:
            candidat = candidat[0]
            nom_affiche = f"{candidat['prenom']} {candidat['nom']} (Extérieur)"
        else:
            nom_affiche = "Inconnu"

    # Charger chien (si présent)
    if chien_id:
        chien = (
            supabase.table("chiens")
            .select("*")
            .eq("id", chien_id)
            .execute()
            .data
        )
        chien = chien[0] if chien else None
    else:
        chien = None

    st.markdown("---")
    st.write(f"👤 **{nom_affiche}**")

    if chien:
        st.write(f"🐶 **{chien['nom']} — {chien['race']}**")
    else:
        st.write("🐶 Aucun chien associé")

    # ---------------------------------------------------------
    # Présence déjà validée ?
    # ---------------------------------------------------------
    if p["present"]:
        st.success("Présence validée ✓")
        continue

    # ---------------------------------------------------------
    # Bouton présence
    # ---------------------------------------------------------
    if st.button(f"Présent n° {p['id']}"):
        
        # Décrémentation abonnement (si membre)
        if membre:
            abo = (
                supabase.table("abonnements")
                .select("*")
                .eq("membre_id", membre_id)
                .eq("actif", True)
                .execute()
                .data
            )

            if abo:
                abo = abo[0]

                # Abonnement à séances
                if abo["seances_restantes"] is not None:
                    nouvelles = abo["seances_restantes"] - 1

                    supabase.table("abonnements").update({
                        "seances_restantes": nouvelles,
                        "actif": nouvelles > 0
                    }).eq("id", abo["id"]).execute()

        # Valider présence
        supabase.table("cours_presences").update({
            "present": True
        }).eq("id", p["id"]).execute()

        st.success(f"{nom_affiche} marqué présent ✓")
        st.rerun()
