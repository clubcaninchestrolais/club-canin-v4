import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

import datetime
from supabase_rest import supabase

st.set_page_config(page_title="Fiche membre", page_icon="👤")

st.title("Fiche membre")

# ---------------------------------------------------------
# FORMAT DATE JJ/MM/AAAA
# ---------------------------------------------------------
def format_date(date_str):
    if not date_str:
        return "N/A"
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    except:
        return date_str

# Déterminer mode création ou édition
if "membre_id" not in st.session_state or st.session_state["membre_id"] is None:
    mode_creation = True

    membre = {
        "prenom": "",
        "nom": "",
        "email": "",
        "telephone": "",
        "telephone2": "",
        "adresse": "",
        "assurance": "",
        "statut": "membre",
        "date_inscription": None,
        "remarques": "",
        "archive": False,
        "code_postal": "",
        "ville": "",
        "police_assurance": "",
        "actif": True
    }

else:
    mode_creation = False
    membre_id = st.session_state["membre_id"]
    membre = supabase.table("membres").select("*").eq("id", membre_id).execute().data[0]

# ---------------------------------------------------------
# GESTION SÉCURISÉE DE LA DATE
# ---------------------------------------------------------

date_raw = membre.get("date_inscription", None)

if isinstance(date_raw, str) and date_raw.strip() == "":
    date_raw = None

if isinstance(date_raw, str):
    try:
        date_raw = datetime.date.fromisoformat(date_raw)
    except:
        date_raw = None

# ---------------------------------------------------------
# FORMULAIRE COMPLET — TOUS LES CHAMPS
# ---------------------------------------------------------

prenom = st.text_input("Prénom", membre.get("prenom", ""))
nom = st.text_input("Nom", membre.get("nom", ""))
email = st.text_input("Email", membre.get("email", ""))
telephone = st.text_input("Téléphone", membre.get("telephone", ""))
telephone2 = st.text_input("Téléphone secondaire", membre.get("telephone2", ""))
adresse = st.text_input("Adresse", membre.get("adresse", ""))
code_postal = st.text_input("Code postal", membre.get("code_postal", ""))
ville = st.text_input("Ville", membre.get("ville", ""))
assurance = st.text_input("Assurance", membre.get("assurance", ""))
police_assurance = st.text_input("Police d’assurance", membre.get("police_assurance", ""))
statut = st.text_input("Statut", membre.get("statut", "membre"))

date_inscription = st.date_input(
    "Date d'inscription",
    date_raw,
    format="DD/MM/YYYY"
)

remarques = st.text_area("Remarques", membre.get("remarques", ""))

actif = st.checkbox("Actif", membre.get("actif", True))
archive = st.checkbox("Archivé", membre.get("archive", False))

st.markdown("---")

# ---------------------------------------------------------
# BOUTON ENREGISTRER
# ---------------------------------------------------------

if st.button("💾 Enregistrer"):
    data = {
        "prenom": prenom,
        "nom": nom,
        "email": email,
        "telephone": telephone,
        "telephone2": telephone2,
        "adresse": adresse,
        "code_postal": code_postal,
        "ville": ville,
        "assurance": assurance,
        "police_assurance": police_assurance,
        "statut": statut,
        "date_inscription": date_inscription.isoformat() if date_inscription else None,
        "remarques": remarques,
        "actif": actif,
        "archive": archive
    }

    if mode_creation:
        supabase.table("membres").insert(data).execute()
        st.success("Membre créé.")
    else:
        supabase.table("membres").update(data).eq("id", membre_id).execute()
        st.success("Membre mis à jour.")

    st.switch_page("pages/01_Membres.py")

if st.button("Retour"):
    st.switch_page("pages/01_Membres.py")

# ---------------------------------------------------------
# CHIENS DU MEMBRE
# ---------------------------------------------------------

st.markdown("---")
st.markdown("## Chiens du membre")

if not mode_creation:
    chiens = supabase.table("chiens").select("*").eq("id_membre", membre_id).execute().data

    if len(chiens) == 0:
        st.info("Ce membre n'a aucun chien enregistré.")
    else:
        for chien in chiens:
            st.write(f"🐶 **{chien['nom']}** — {chien['race']}")

            if st.button(f"📄 Voir fiche chien — {chien['nom']}", key=f"chien_{chien['id']}"):
                st.session_state["chien_id"] = chien["id"]
                st.session_state["retour_membre"] = True
                st.switch_page("pages/_fiche_chien_page.py")

# ---------------------------------------------------------
# COTISATIONS
# ---------------------------------------------------------

st.markdown("---")
st.markdown("## Cotisations")

if not mode_creation:
    cotisations = supabase.table("cotisations").select("*").eq("membre_id", membre_id).execute().data

    st.write(f"📊 **Nombre de cotisations : {len(cotisations)}**")

    if len(cotisations) == 0:
        st.info("Aucune cotisation enregistrée.")
    else:
        for c in cotisations:
            st.write(f"""
            💶 **Montant :** {c.get('montant', 'N/A')}  
            📅 **Date de paiement :** {format_date(c.get('date_paiement'))}  
            ⏳ **Expiration :** {format_date(c.get('date_expiration'))}  
            🏷️ **Type :** {c.get('type', 'N/A')}  
            🔖 **Statut :** {c.get('statut', 'N/A')}  
            📝 **Remarques :** {c.get('remarques', 'N/A')}
            """)

# ---------------------------------------------------------
# ABONNEMENTS
# ---------------------------------------------------------

st.markdown("---")
st.markdown("## Abonnements")

if not mode_creation:
    abonnements = supabase.table("abonnements").select("*").eq("membre_id", membre_id).execute().data

    st.write(f"📊 **Nombre d’abonnements : {len(abonnements)}**")

    if len(abonnements) == 0:
        st.info("Aucun abonnement enregistré.")
    else:
        for a in abonnements:
            actif_ab = "🟢 Actif" if a.get("actif", False) else "🔴 Inactif / Expiré"

            st.write(f"""
            📘 **Type :** {a.get('type', 'N/A')}  
            💶 **Prix :** {a.get('prix', 'N/A')}  
            🔢 **Séances totales :** {a.get('seances_total', 'N/A')}  
            🔢 **Séances restantes :** {a.get('seances_restantes', 'N/A')}  
            📅 **Date d'achat :** {format_date(a.get('date_achat'))}  
            ⏳ **Expiration :** {format_date(a.get('expiration'))}  
            {actif_ab}  
            📝 **Note :** {a.get('note', 'N/A')}
            """)

# ---------------------------------------------------------
# ⭐ AJOUT : BOUTON HISTORIQUE DES PRÉSENCES
# ---------------------------------------------------------

if not mode_creation:
    st.markdown("---")
    st.markdown("## Historique des présences")

    if st.button("📅 Voir l’historique des présences", key=f"histo_{membre_id}"):
        st.session_state["historique_membre_id"] = membre_id
        st.switch_page("pages/XX_Historique_Presences.py")
