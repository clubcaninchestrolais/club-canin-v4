import streamlit as st
from supabase_rest import supabase
from datetime import datetime, date

st.set_page_config(page_title="Fiche Cotisation", page_icon="💳")
st.title("💳 Fiche Cotisation")

# ---------------------------------------------------------
# Vérifier qu’un ID est présent
# ---------------------------------------------------------
if "cot_id" not in st.session_state:
    st.error("Aucune cotisation sélectionnée.")
    st.stop()

cot_id = st.session_state["cot_id"]

# ---------------------------------------------------------
# Charger la cotisation
# ---------------------------------------------------------
cot = (
    supabase.table("cotisations")
    .select("*")
    .eq("id", cot_id)
    .execute()
    .data
)

if not cot:
    st.error("Cotisation introuvable.")
    st.stop()

cot = cot[0]

# ---------------------------------------------------------
# Charger le membre (CORRECTION ICI : membre_id)
# ---------------------------------------------------------
membre = (
    supabase.table("membres")
    .select("*")
    .eq("id", cot["membre_id"])
    .execute()
    .data
)

if membre:
    membre = membre[0]
    nom = membre["nom"]
    prenom = membre["prenom"]
else:
    nom = "Inconnu"
    prenom = ""

# ---------------------------------------------------------
# Fonction date sécurisée
# ---------------------------------------------------------
def safe_date(value):
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "")).strftime("%d/%m/%Y")
        except:
            return ""
    return ""

date_pay = safe_date(cot.get("date_paiement"))
date_exp = safe_date(cot.get("date_expiration"))

# ---------------------------------------------------------
# Affichage
# ---------------------------------------------------------
st.subheader("📄 Informations de la cotisation")

st.markdown(f"""
**Membre :** {nom} {prenom}  
**Montant :** {cot['montant']} €  
**Type :** {cot['type']}  
**Payée le :** {date_pay}  
**Expire le :** {date_exp}  
""")

st.markdown("---")

# ---------------------------------------------------------
# Bouton retour
# ---------------------------------------------------------
if st.button("⬅️ Retour aux cotisations"):
    st.switch_page("pages/20_Cotisations.py")
