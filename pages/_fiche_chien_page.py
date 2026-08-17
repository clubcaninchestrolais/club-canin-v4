import streamlit as st
from supabase_rest import supabase

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
race = st.text_input("Raceduchien", chien["race"])

sexe = st.text_input("Sexe", chien["sexe"])
date_naissance = st.date_input("Date de naissance", chien["date_naissance"]) if chien["date_naissance"] else st.date_input("Date de naissance")
age = st.number_input("Âge", value=chien.get("age", 0))

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

    # Supprimer l’ancienne photo si elle existe
    try:
        bucket.remove([file_name])
    except Exception:
        pass

    # Upload du nouveau fichier
    bucket.upload(file_name, file_bytes)

    # URL publique
    photo_url = bucket.get_public_url(file_name)

    st.success("Photo téléversée avec succès !")

# Affichage de la photo si présente
if photo_url:
    st.image(photo_url, caption=f"Photo de {nom}", width=250)

st.markdown("---")

# Actif = non archivé
actif = st.checkbox("Actif", not chien.get("archive", False))

# Bouton enregistrer
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

# Bouton retour
if st.button("Retour"):
    st.switch_page("pages/02_Chiens.py")
