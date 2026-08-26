import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from supabase_rest import supabase
from datetime import date

st.set_page_config(page_title="Fiche chien", page_icon="🐾")

st.title("Fiche chien")

# Déterminer mode création ou édition
if "chien_id" not in st.session_state or st.session_state["chien_id"] is None:
    mode_creation = True
    chien = {
        "nom": "",
        "race": "",
        "sexe": "",
        "date_naissance": None,
        "numero_puce": "",
        "numero_carnet": "",
        "identification": "",
        "remarques": "",
        "age": 0,
        "photo_url": "",
        "id_membre": None,
        "archive": False
    }
else:
    mode_creation = False
    chien_id = st.session_state["chien_id"]
    chien = supabase.table("chiens").select("*").eq("id", chien_id).execute().data[0]

# Charger les membres
membres = supabase.table("membres").select("*").execute().data

# Trouver l’index du membre actuel
if chien["id_membre"] is None:
    index_membre = 0
else:
    index_membre = next(
        (i for i, m in enumerate(membres) if m["id"] == chien["id_membre"]),
        0
    )

proprietaire = st.selectbox(
    "Propriétaire",
    membres,
    format_func=lambda m: f"{m['prenom']} {m['nom']}",
    index=index_membre
)

st.markdown("### Informations générales")

nom = st.text_input("Nom du chien", chien["nom"])
race = st.text_input("Race", chien["race"])

# --- SEXE : choix Mâle / Femelle ---
sexe_options = ["Mâle", "Femelle"]
sexe = st.selectbox(
    "Sexe",
    sexe_options,
    index=sexe_options.index(chien["sexe"]) if chien["sexe"] in sexe_options else 0
)

# --- DATE DE NAISSANCE ---
date_naissance = (
    st.date_input("Date de naissance", chien["date_naissance"])
    if chien["date_naissance"]
    else st.date_input("Date de naissance")
)

# --- CALCUL AUTOMATIQUE DE L'ÂGE ---
def calcul_age(dn):
    if not dn:
        return 0
    today = date.today()
    return today.year - dn.year - ((today.month, today.day) < (dn.month, dn.day))

age = calcul_age(date_naissance)
st.write(f"Âge : {age} ans")

st.markdown("### Identification")

numero_puce = st.text_input("Numéro de puce", chien["numero_puce"])
numero_carnet = st.text_input("Numéro de carnet", chien["numero_carnet"])
identification = st.text_input("Identification", chien["identification"])

st.markdown("### Remarques")

remarques = st.text_area("Remarques", chien["remarques"])

st.markdown("### Photo")

photo_url = st.text_input("URL de la photo", chien["photo_url"])

uploaded_photo = st.file_uploader("Téléverser une photo", type=["png", "jpg", "jpeg"])

if uploaded_photo:
    file_bytes = uploaded_photo.read()
    file_name = f"chien_{nom.replace(' ', '_')}.jpg"

    bucket = supabase.storage.from_("photos_chiens")

    try:
        bucket.remove([file_name])
    except Exception:
        pass

    bucket.upload(file_name, file_bytes)
    photo_url = bucket.get_public_url(file_name)

    st.success("Photo téléversée avec succès !")

if photo_url:
    st.image(photo_url, caption=f"Photo de {nom}", width=250)

st.markdown("---")

actif = st.checkbox("Actif", not chien.get("archive", False))

if st.button("💾 Enregistrer"):
    data = {
        "nom": nom,
        "race": race,
        "sexe": sexe,
        "date_naissance": date_naissance.isoformat(),
        "numero_puce": numero_puce,
        "numero_carnet": numero_carnet,
        "identification": identification,
        "remarques": remarques,
        "age": age,
        "photo_url": photo_url,
        "id_membre": proprietaire["id"],
        "archive": not actif
    }

    if mode_creation:
        supabase.table("chiens").insert(data).execute()
        st.success("Chien créé.")
    else:
        supabase.table("chiens").update(data).eq("id", chien_id).execute()
        st.success("Chien mis à jour.")

    st.switch_page("pages/02_Chiens.py")

if st.button("Retour"):
    st.switch_page("pages/02_Chiens.py")
