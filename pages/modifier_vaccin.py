import streamlit as st
from securite import securite_admin
securite_admin()

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral
from datetime import date

hide_streamlit_menu()
menu_lateral()

st.title("✏️ Modifier un vaccin")

# Vérifier qu’un vaccin est sélectionné
if "vaccin_id" not in st.session_state or st.session_state["vaccin_id"] is None:
    st.error("Aucun vaccin sélectionné.")
    st.stop()

vaccin_id = st.session_state["vaccin_id"]

# Charger le vaccin
result = (
    supabase.table("vaccins")
    .select("*")
    .eq("id", vaccin_id)
    .execute()
)

if not result.data:
    st.error("Vaccin introuvable.")
    st.stop()

vaccin = result.data[0]

# Charger le chien
chien = (
    supabase.table("chiens")
    .select("*")
    .eq("id", vaccin["chien_id"])
    .execute()
    .data[0]
)

st.write(f"🐶 **Chien : {chien['nom']}**")
st.markdown("---")

# Champs modifiables
nom_vaccin = st.text_input("Nom du vaccin", vaccin["nom_vaccin"])

date_vaccin = st.date_input(
    "Date du vaccin",
    date.fromisoformat(vaccin["date_vaccin"])
)

valid_until = st.date_input(
    "Date de fin de validité",
    date.fromisoformat(vaccin["valid_until"]) if vaccin.get("valid_until") else date.today()
)

remarques = st.text_area("Remarques", vaccin.get("remarques", ""))

# Bouton enregistrer
if st.button("💾 Enregistrer les modifications"):
    supabase.table("vaccins").update({
        "nom_vaccin": nom_vaccin,
        "date_vaccin": str(date_vaccin),
        "valid_until": str(valid_until),
        "remarques": remarques
    }).eq("id", vaccin_id).execute()

    st.success("Vaccin mis à jour avec succès.")
    st.switch_page("pages/vaccins.py")

# Bouton retour
if st.button("⬅️ Retour"):
    st.switch_page("pages/vaccins.py")
