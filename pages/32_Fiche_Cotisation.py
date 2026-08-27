import streamlit as st
from supabase_rest import supabase
from datetime import datetime, date
from menu import hide_streamlit_menu, menu_lateral

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="Fiche cotisation", page_icon="📄", layout="wide")
hide_streamlit_menu()
menu_lateral()

st.title("📄 Détail de la cotisation")

# ---------------------------------------------------------
# Charger la cotisation sélectionnée
# ---------------------------------------------------------
cot_id = st.session_state.get("cot_id", None)

if cot_id is None:
    st.error("Aucune cotisation sélectionnée.")
    st.stop()

cot = (
    supabase.table("cotisations")
    .select("*")
    .eq("id", cot_id)
    .execute()
    .data[0]
)

# ---------------------------------------------------------
# Affichage des informations
# ---------------------------------------------------------
st.subheader("📌 Informations générales")

date_pay = cot.get("date_paiement")
mode_pay = cot.get("mode_de_paiement")

st.write(f"**Montant :** {cot['montant']} €")
st.write(f"**Type :** {cot['type']}")
st.write(f"**Payé :** {'Oui' if cot['paye'] else 'Non'}")
st.write(f"**Date paiement :** {date_pay if date_pay else '—'}")
st.write(f"**Mode de paiement :** {mode_pay if mode_pay else '—'}")
st.write(f"**Expiration :** {cot['date_expiration']}")

st.markdown("---")

# ---------------------------------------------------------
# Mise à jour du paiement
# ---------------------------------------------------------
st.subheader("💰 Paiement")

# Champ mode de paiement
mode_de_paiement = st.selectbox(
    "Mode de paiement",
    ["cash", "virement", "QRCode"],
    index=0 if mode_pay is None else ["cash", "virement", "QRCode"].index(mode_pay)
)

# Champ date de paiement
if date_pay:
    try:
        date_paiement_init = datetime.fromisoformat(date_pay).date()
    except:
        date_paiement_init = date.today()
else:
    date_paiement_init = date.today()

date_paiement = st.date_input("Date de paiement", value=date_paiement_init)

# Bouton de mise à jour
if st.button("Mettre à jour le paiement"):
    supabase.table("cotisations").update({
        "paye": True,
        "date_paiement": str(date_paiement),
        "mode_de_paiement": mode_de_paiement
    }).eq("id", cot_id).execute()

    st.success("Paiement mis à jour.")
    st.rerun()

st.markdown("---")

# Bouton retour
if st.button("⬅ Retour"):
    st.switch_page("pages/20_Cotisations.py")
