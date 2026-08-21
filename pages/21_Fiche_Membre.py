import streamlit as st
from supabase import create_client

# ---------------------------------------------------------
# Récupération de l'ID membre via session_state
# ---------------------------------------------------------
membre_id = st.session_state.get("membre_id")

if not membre_id:
    st.error("Aucun membre sélectionné.")
    st.stop()

# ---------------------------------------------------------
# Connexion Supabase (sécurisée)
# ---------------------------------------------------------
url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")

if not url or not key:
    st.error("⚠️ Erreur : les secrets SUPABASE ne sont pas disponibles.")
    st.stop()

supabase = create_client(url, key)

# ---------------------------------------------------------
# Charger le membre
# ---------------------------------------------------------
m = (
    supabase.table("membres")
    .select("*")
    .eq("id", membre_id)
    .execute()
    .data[0]
)

# ---------------------------------------------------------
# Affichage du membre
# ---------------------------------------------------------
st.title(f"{m['prenom']} {m['nom']}")

# Badge TEMPORAIRE (disparaît automatiquement si temporaire=False)
if m.get("temporaire", False):
    st.markdown(
        "<div style='background:red;color:white;padding:10px;border-radius:6px;"
        "font-weight:bold;width:180px;text-align:center;font-size:18px;'>TEMPORAIRE</div>",
        unsafe_allow_html=True
    )

st.write(f"📧 Email : {m.get('email', '')}")
st.write(f"📱 Téléphone : {m.get('telephone', '')}")

st.markdown("---")
st.subheader("🐶 Chien")

# ---------------------------------------------------------
# Charger le chien
# ---------------------------------------------------------
chiens = (
    supabase.table("chiens")
    .select("*")
    .eq("id_membre", membre_id)
    .execute()
    .data
)

if chiens:
    c = chiens[0]
    st.write(f"Nom : {c['nom']}")
    st.write(f"Race : {c['race']}")
    st.write(f"Date de naissance : {c['date_naissance']}")
else:
    st.info("Aucun chien enregistré.")

# ---------------------------------------------------------
# FORMULAIRE DE MODIFICATION DU MEMBRE
# ---------------------------------------------------------
st.markdown("---")
st.subheader("✏️ Modifier le membre")

with st.form("form_modif_membre"):

    prenom = st.text_input("Prénom", m.get("prenom", ""))
    nom = st.text_input("Nom", m.get("nom", ""))
    email = st.text_input("Email", m.get("email", ""))
    telephone = st.text_input("Téléphone", m.get("telephone", ""))
    telephone2 = st.text_input("Téléphone secondaire", m.get("telephone2", ""))
    adresse = st.text_input("Adresse", m.get("adresse", ""))
    code_postal = st.text_input("Code postal", m.get("code_postal", ""))
    ville = st.text_input("Ville", m.get("ville", ""))

    statut = st.selectbox(
        "Statut",
        ["membre", "benevole"],
        index=0 if m.get("statut") == "membre" else 1
    )

    assurance = st.text_input("Assurance", m.get("assurance", ""))
    police_assurance = st.text_input("Police d’assurance", m.get("police_assurance", ""))
    remarques = st.text_area("Remarques", m.get("remarques", ""))

    actif = st.checkbox("Actif", m.get("actif", True))
    archive = st.checkbox("Archivé", m.get("archive", False))

    submit = st.form_submit_button("💾 Enregistrer les modifications")

if submit:
    supabase.table("membres").update({
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
        "remarques": remarques,
        "actif": actif,
        "archive": archive
    }).eq("id", membre_id).execute()

    st.success("Modifications enregistrées ✔")
    st.rerun()

# ---------------------------------------------------------
# Actions du préposé
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📌 Actions du préposé")

# Confirmer affiliation (corrigé : retire TEMPORAIRE automatiquement)
if m.get("temporaire", False):
    if st.button("Confirmer affiliation"):
        supabase.table("membres").update({
            "temporaire": False,
            "statut": "membre",
            "affilie": True
        }).eq("id", membre_id).execute()

        st.success("Affiliation confirmée ✔")
        st.rerun()

# Supprimer membre
#if st.button("Supprimer membre"):

    #supabase.table("cours_presences").delete().eq("membre_id", membre_id).execute()
    #supabase.table("cours_inscriptions").delete().eq("membre_id", membre_id).execute()
    #supabase.table("chiens").delete().eq("id_membre", membre_id).execute()
    #supabase.table("membres").delete().eq("id", membre_id).execute()

    #st.success("Membre supprimé ✔")
    #st.stop()
