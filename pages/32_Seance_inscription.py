import streamlit as st
from datetime import date, datetime
from supabase_rest import supabase

st.set_page_config(page_title="Inscription séance", page_icon="🐾")
st.title("🐾 Inscription à une séance")

# ---------------------------------------------------------
# Fonction robuste pour convertir une date
# ---------------------------------------------------------
def safe_date(v):
    if v is None:
        return None
    if isinstance(v, date):
        return v
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, str):
        try:
            return date.fromisoformat(v)
        except:
            return None
    return None

# ---------------------------------------------------------
# Récupération du membre
# ---------------------------------------------------------
params = st.query_params
membre_id = params.get("membre_id", None) or st.session_state.get("membre_id")

if not membre_id:
    st.error("Aucun membre sélectionné.")
    st.stop()

# ---------------------------------------------------------
# Afficher le membre
# ---------------------------------------------------------
membre = (
    supabase.table("membres")
    .select("*")
    .eq("id", membre_id)
    .execute()
    .data
)

if not membre:
    st.error("Membre introuvable.")
    st.stop()

membre = membre[0]
st.subheader("👤 Membre")
st.write(f"**{membre['prenom']} {membre['nom']}**")

# ---------------------------------------------------------
# Afficher le chien (si sélectionné)
# ---------------------------------------------------------
chien_id = st.session_state.get("chien_id")

if chien_id:
    chien = (
        supabase.table("chiens")
        .select("*")
        .eq("id", chien_id)
        .execute()
        .data
    )
    if chien:
        chien = chien[0]
        st.write(f"🐶 **Chien : {chien['nom']}**")

# ---------------------------------------------------------
# Charger l'abonnement du membre
# ---------------------------------------------------------
abos = (
    supabase.table("abonnements")
    .select("*")
    .eq("id_membre", membre_id)
    .order("id", desc=True)
    .execute()
    .data
)

if not abos:
    st.warning("Ce membre n'a aucun abonnement.")
    st.stop()

abo = abos[0]

seances_total = abo.get("seances_total", 0)
seances_restantes = abo.get("seances_restantes", 0)

# ---------------------------------------------------------
# Vérification abonnement
# ---------------------------------------------------------
if seances_total != -1 and seances_restantes <= 0:
    st.error("⛔ Abonnement épuisé : aucune séance restante.")
    st.stop()

# ---------------------------------------------------------
# Affichage des séances déjà inscrites
# ---------------------------------------------------------
st.subheader("📅 Séances déjà inscrites")

presences = (
    supabase.table("cours_presences")
    .select("id, cours_id, date_presence, chien_id")
    .eq("membre_id", membre_id)
    .order("date_presence")
    .execute()
    .data
)

if not presences:
    st.info("Aucune séance inscrite pour ce membre.")
else:
    for p in presences:

        # Récupérer infos du cours
        cours = (
            supabase.table("cours_seances")
            .select("date_seance, heure_debut")
            .eq("cours_id", p["cours_id"])
            .eq("date_seance", p["date_presence"])
            .execute()
            .data
        )

        if cours:
            c = cours[0]
            st.write(
                f"🗓 **{c['date_seance']} — {c['heure_debut']}** (cours {p['cours_id']})"
            )
        else:
            st.write(
                f"🗓 {p['date_presence']} (cours {p['cours_id']})"
            )

        # Récupérer le chien
        if p["chien_id"]:
            chien = (
                supabase.table("chiens")
                .select("nom")
                .eq("id", p["chien_id"])
                .execute()
                .data
            )
            if chien:
                st.write(f"🐶 Chien : **{chien[0]['nom']}**")

        # Bouton désinscription
        if st.button(f"Désinscrire (id {p['id']})", key=f"del_{p['id']}"):
            supabase.table("cours_presences").delete().eq("id", p["id"]).execute()
            st.success("Séance supprimée.")
            st.rerun()

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

choix = st.selectbox(
    "Séance à inscrire",
    options=seances,
    format_func=lambda s: f"{s['date_seance']} — {s['heure_debut']} (cours {s['cours_id']})"
)

# ---------------------------------------------------------
# Inscription
# ---------------------------------------------------------
if st.button("Inscrire le membre à cette séance"):

    # Convertir la date proprement → en string ISO
    date_presence = safe_date(choix["date_seance"])
    if not date_presence:
        st.error("Date de séance invalide.")
        st.stop()

    date_iso = date_presence.isoformat()

    # Vérification anti-doublon
    deja = (
        supabase.table("cours_presences")
        .select("*")
        .eq("membre_id", membre_id)
        .eq("cours_id", choix["cours_id"])
        .eq("date_presence", date_iso)
        .execute()
        .data
    )

    if deja:
        st.warning("Ce membre est déjà inscrit à cette séance.")
        st.stop()

    # Inscription (sans décrémentation)
    supabase.table("cours_presences").insert({
        "membre_id": membre_id,
        "cours_id": choix["cours_id"],
        "chien_id": chien_id,
        "date_presence": date_iso,
        "statut": "absent"
    }).execute()

    st.success("Inscription enregistrée !")
