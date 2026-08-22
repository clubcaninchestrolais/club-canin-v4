import streamlit as st
from supabase_rest import supabase
from datetime import datetime, date, timedelta

st.set_page_config(page_title="Fiche Cotisation", page_icon="📄")
st.title("📄 Fiche Cotisation")

# ---------------------------------------------------------
# Fonction de conversion sécurisée
# ---------------------------------------------------------
def safe_date(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, str) and value.strip() != "":
        try:
            return datetime.fromisoformat(value.replace("Z", ""))
        except:
            return None
    return None

# ---------------------------------------------------------
# Vérifier que l’ID est présent
# ---------------------------------------------------------
cot_id = st.session_state.get("cot_id", None)

if cot_id is None:
    st.error("Aucune cotisation sélectionnée.")
    st.stop()

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

# Charger le membre
membre = (
    supabase.table("membres")
    .select("*")
    .eq("id", cot["membre_id"])
    .execute()
    .data
)

membre = membre[0] if membre else None

# ---------------------------------------------------------
# Préparer les dates
# ---------------------------------------------------------
date_pay = safe_date(cot.get("date_paiement"))
date_exp = safe_date(cot.get("date_expiration"))

# ---------------------------------------------------------
# Déterminer la couleur
# ---------------------------------------------------------
if cot.get("paye"):
    couleur = "#e6ffe6"  # vert = payé
else:
    if date_exp:
        jours_restants = (date_exp - datetime.now()).days
        if jours_restants < 0:
            couleur = "#ffcccc"  # rouge = expirée impayée
        elif jours_restants <= 30:
            couleur = "#ffe6cc"  # orange = bientôt expirée impayée
        else:
            couleur = "#ffcccc"
    else:
        couleur = "#ffcccc"

# ---------------------------------------------------------
# Affichage
# ---------------------------------------------------------
st.markdown(
    f"<div style='background:{couleur};padding:10px;border-radius:6px;'>"
    f"<b>{membre['nom']} {membre['prenom']}</b><br>"
    f"Montant : {cot['montant']} €<br>"
    f"Type : {cot['type']}<br>"
    f"Payé : {'Oui' if cot.get('paye') else 'Non'}<br>"
    f"Date paiement : {date_pay.strftime('%d/%m/%Y') if date_pay else '—'}<br>"
    f"Expiration : {date_exp.strftime('%d/%m/%Y') if date_exp else '—'}"
    f"</div>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------------------------------------------------
# Modification du paiement
# ---------------------------------------------------------
st.subheader("💰 Paiement")

paye = st.checkbox("Le membre a payé", value=cot.get("paye", False))

if paye:
    new_date_pay = st.date_input(
        "Date de paiement",
        value=date_pay.date() if date_pay else date.today()
    )

    # 🔥 Calcul automatique de la date d'expiration
    new_exp = new_date_pay + timedelta(days=365)

else:
    new_date_pay = None
    new_exp = st.date_input(
        "Date d'expiration (provisoire si impayé)",
        value=date_exp.date() if date_exp else date.today()
    )

if st.button("Mettre à jour le paiement"):
    supabase.table("cotisations").update({
        "paye": paye,
        "date_paiement": str(new_date_pay) if new_date_pay else None,
        "date_expiration": str(new_exp)
    }).eq("id", cot_id).execute()

    st.success("Paiement mis à jour.")
    st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Remarques
# ---------------------------------------------------------
st.subheader("📝 Remarques")

new_rem = st.text_area("Remarques", cot.get("remarques", ""))

if st.button("Mettre à jour les remarques"):
    supabase.table("cotisations").update({
        "remarques": new_rem
    }).eq("id", cot_id).execute()

    st.success("Remarques mises à jour.")
    st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Retour
# ---------------------------------------------------------
if st.button("⬅️ Retour"):
    st.switch_page("pages/31_Cotisations.py")


