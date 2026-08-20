import streamlit as st
from supabase import create_client

# 🔗 Connexion Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.set_page_config(page_title="Validation des présences", page_icon="📋")
st.title("📋 Validation des présences")

# 1️⃣ Charger les séances
seances = (
    supabase.table("cours_seances")
    .select("*")
    .order("date_seance")
    .execute()
    .data
)

if not seances:
    st.error("Aucune séance trouvée.")
    st.stop()

# Selectbox robuste (évite les KeyError)
liste = {
    f"{s.get('id', '?')} — {s.get('date_seance', '?')}": s["id"]
    for s in seances
}
choix = st.selectbox("Séance :", list(liste.keys()), key="select_seance_70")
seance_id = liste[choix]

# 2️⃣ Charger les présences de la séance
presences = (
    supabase.table("cours_presences")
    .select("*")
    .eq("seance_id", seance_id)
    .execute()
    .data
)

st.subheader("Présences à valider")

if not presences:
    st.info("Aucune présence pour cette séance.")
    st.stop()

for index, p in enumerate(presences):

    presence_id = p["id"]
    membre_id = p["membre_id"]
    chien_id = p["chien_id"]
    present = p["present"]

    # 3️⃣ Charger le membre (robuste pour extérieurs)
    nom = "Extérieur"

    if membre_id is not None:
        membre_data = (
            supabase.table("membres")
            .select("*")
            .eq("id", membre_id)
            .execute()
            .data
        )
        if membre_data:
            membre = membre_data[0]
            nom = f"{membre.get('prenom', '')} {membre.get('nom', '')}".strip()

    st.write(f"**{nom}** — ID présence {presence_id}")

    bouton_key = f"btn_{presence_id}_{index}"

    if not present:
        if st.button(f"Présent n° {presence_id}", key=bouton_key):

            # 4️⃣ Marquer la présence comme validée
            supabase.table("cours_presences").update(
                {
                    "present": True,
                    "date_presence": p.get("date_presence"),
                }
            ).eq("id", presence_id).execute()

            # 5️⃣ Si c'est un vrai membre → gestion abonnement + inscription
            if membre_id is not None:
                inscription_existante = (
                    supabase.table("cours_seances_inscriptions")
                    .select("*")
                    .eq("membre_id", membre_id)
                    .eq("seance_id", seance_id)
                    .execute()
                    .data
                )

                if not inscription_existante:
                    abo = (
                        supabase.table("abonnements")
                        .select("*")
                        .eq("membre_id", membre_id)
                        .eq("actif", True)
                        .execute()
                        .data
                    )

                    if abo:
                        abonnement = abo[0]
                        reste = abonnement.get("seances_restantes")

                        if reste is not None and reste > 0:
                            supabase.table("abonnements").update(
                                {"seances_restantes": reste - 1}
                            ).eq("id", abonnement["id"]).execute()

                    data_inscription = {
                        "membre_id": membre_id,
                        "seance_id": seance_id,
                    }
                    if chien_id is not None:
                        data_inscription["chien_id"] = chien_id

                    supabase.table("cours_seances_inscriptions").insert(
                        data_inscription
                    ).execute()

            # 6️⃣ Extérieurs : pas de décrémentation, mais présence validée
            st.success("Présence validée ✔")
            st.rerun()

    else:
        st.write("✔ Déjà validé")

