import streamlit as st
from securite import securite_user
securite_user()

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral


st.set_page_config(page_title="Cours du jour", page_icon="📅")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("📅 Cours du jour")

# ---------------------------------------------------------
# 1. Trouver les séances actives FUTURES
# ---------------------------------------------------------

today = date.today().isoformat()

seances_raw = (
    supabase.table("cours_seances")
    .select("*")
    .eq("actif", True)
    .order("date_seance", desc=False)
    .execute()
    .data
)

# Filtrage Python
seances = [
    s for s in seances_raw
    if s["date_seance"]
    and isinstance(s["date_seance"], str)
    and len(s["date_seance"]) == 10
    and s["date_seance"] >= today
]

if not seances:
    st.warning("Aucune séance future active trouvée.")
    st.stop()

# Prendre la première séance future
seance = seances[0]

st.subheader(f"Séance du {seance['date_seance']}")

# ---------------------------------------------------------
# 2. Charger le cours lié à cette séance
# ---------------------------------------------------------
cours = (
    supabase.table("cours")
    .select("*")
    .eq("id", seance["cours_id"])
    .execute()
    .data
)

if not cours:
    st.info("Aucun cours trouvé pour cette séance.")
    st.stop()

cours = cours[0]

st.markdown("---")
st.write(f"### 🐾 {cours['categorie']} (ID {cours['id']})")

# ---------------------------------------------------------
# 3. INSCRIPTION DIRECTE À LA SÉANCE
# ---------------------------------------------------------
st.markdown("### ➕ Inscrire un chien à cette séance")

# Charger les membres
membres = (
    supabase.table("membres")
    .select("*")
    .order("prenom")
    .execute()
    .data
)

membre_select = st.selectbox(
    "Choisir un membre",
    membres,
    format_func=lambda m: f"{m['prenom']} {m['nom']}"
)

# Charger les chiens du membre
chiens = (
    supabase.table("chiens")
    .select("*")
    .eq("id_membre", membre_select["id"])
    .execute()
    .data
)

if not chiens:
    st.info("Ce membre n'a aucun chien enregistré.")
else:
    chien_select = st.selectbox(
        "Choisir un chien",
        chiens,
        format_func=lambda c: f"{c['nom']} ({c['race']})"
    )

    # Vérifier si déjà inscrit (cours_inscriptions)
    deja_inscrit = (
        supabase.table("cours_inscriptions")
        .select("*")
        .eq("seance_id", seance["id"])
        .eq("chien_id", chien_select["id"])
        .execute()
        .data
    )

    if deja_inscrit:
        st.warning("⚠️ Ce chien est déjà inscrit à cette séance.")
    else:
        if st.button("Inscrire ce chien"):
            supabase.table("cours_inscriptions").insert({
                "seance_id": seance["id"],
                "membre_id": membre_select["id"],
                "chien_id": chien_select["id"],
                "statut": "inscrit",
                "type": "normal",
                "date_inscription": date.today().isoformat()
            }).execute()

            st.success(f"🐶 {chien_select['nom']} a été inscrit à la séance.")
            st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# 4. Charger les inscrits via cours_inscriptions
# ---------------------------------------------------------
inscrits_raw = (
    supabase.table("cours_inscriptions")
    .select("*")
    .eq("seance_id", seance["id"])
    .execute()
    .data
)

st.markdown("### 👥 Chiens inscrits")

# ---------------------------------------------------------
# 5. Afficher les inscrits
# ---------------------------------------------------------
if not inscrits_raw:
    st.info("Aucun inscrit pour cette séance.")
else:
    for ins in inscrits_raw:

        # Charger le membre
        membre = (
            supabase.table("membres")
            .select("*")
            .eq("id", ins["membre_id"])
            .execute()
            .data[0]
        )

        # Charger le chien
        chien = (
            supabase.table("chiens")
            .select("*")
            .eq("id", ins["chien_id"])
            .execute()
            .data[0]
        )

        st.write(
            f"- **{membre['prenom']} {membre['nom']}** — "
            f"{chien['nom']} ({chien['race']})"
        )

