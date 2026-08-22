import streamlit as st
from supabase_rest import supabase
from datetime import datetime, date, timedelta

st.set_page_config(page_title="Fiche Abonnement", page_icon="📄")
st.title("📄 Détail de l'abonnement")

# ---------------------------------------------------------
# Vérifier que l’ID est présent
# ---------------------------------------------------------
if "abo_id" not in st.session_state:
    st.error("Aucun abonnement sélectionné.")
    st.stop()

abo_id = st.session_state["abo_id"]

# ---------------------------------------------------------
# Charger l’abonnement
# ---------------------------------------------------------
abo = (
    supabase.table("abonnements")
    .select("*")
    .eq("id", abo_id)
    .execute()
    .data
)

if not abo:
    st.error("Abonnement introuvable.")
    st.stop()

abo = abo[0]

# ---------------------------------------------------------
# Charger le membre lié
# ---------------------------------------------------------
membre = (
    supabase.table("membres")
    .select("*")
    .eq("id", abo["membre_id"])
    .execute()
    .data[0]
)

# ---------------------------------------------------------
# Préparer les dates
# ---------------------------------------------------------
def safe_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", ""))
    except:
        return None

date_pay = safe_date(abo.get("date_paiement"))
date_exp = safe_date(abo.get("date_expiration"))

# ---------------------------------------------------------
# Déterminer la couleur
# ---------------------------------------------------------
if abo.get("paye"):
    couleur = "#e6ffe6"  # vert
else:
    if date_exp:
        jours = (date_exp - datetime.now()).days
        if jours < 0:
            couleur = "#ffcccc"  # rouge
        elif jours <= 30:
            couleur = "#ffe6cc"  # orange
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
    f"Total séances : {abo['seances_total']}<br>"
    f"Séances restantes : {abo['seances_restantes']}<br>"
    f"Prix : {abo['prix']} €<br>"
    f"Payé : {'Oui' if abo.get('paye') else 'Non'}<br>"
    f"Date paiement : {date_pay.strftime('%d/%m/%Y') if date_pay else '—'}<br>"
    f"Expiration : {date_exp.strftime('%d/%m/%Y') if date_exp else '—'}<br>"
    f"Actif : {'Oui' if abo['actif'] else 'Non'}"
    f"</div>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------------------------------------------------
# Paiement
# ---------------------------------------------------------
st.subheader("💰 Paiement")

paye = st.checkbox("Le membre a payé", value=abo.get("paye", False))

if paye:
    new_date_pay = st.date_input(
        "Date de paiement",
        value=date_pay.date() if date_pay else date.today()
    )
    new_exp = new_date_pay + timedelta(days=365)
else:
    new_date_pay = None
    new_exp = st.date_input(
        "Date d'expiration",
        value=date_exp.date() if date_exp else date.today()
    )

if st.button("Mettre à jour le paiement"):
    supabase.table("abonnements").update({
        "paye": paye,
        "date_paiement": str(new_date_pay) if new_date_pay else None,
        "date_expiration": str(new_exp)
    }).eq("id", abo_id).execute()

    st.success("Paiement mis à jour.")
    st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Boutons +1 / -1
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Ajouter une séance"):
        supabase.table("abonnements").update({
            "seances_restantes": abo["seances_restantes"] + 1
        }).eq("id", abo_id).execute()
        st.success("Séance ajoutée.")
        st.rerun()

with col2:
    if st.button("➖ Retirer une séance"):
        if abo["seances_restantes"] > 0:
            supabase.table("abonnements").update({
                "seances_restantes": abo["seances_restantes"] - 1
            }).eq("id", abo_id).execute()
            st.success("Séance retirée.")
            st.rerun()
        else:
            st.warning("Impossible : aucune séance restante.")

st.markdown("---")

# ---------------------------------------------------------
# Activation / désactivation
# ---------------------------------------------------------
if abo["actif"]:
    if st.button("🔴 Désactiver l'abonnement"):
        supabase.table("abonnements").update({"actif": False}).eq("id", abo_id).execute()
        st.success("Abonnement désactivé.")
        st.rerun()
else:
    if st.button("🟢 Réactiver l'abonnement"):
        supabase.table("abonnements").update({"actif": True}).eq("id", abo_id).execute()
        st.success("Abonnement réactivé.")
        st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# Retour FIABLE
# ---------------------------------------------------------
if st.button("⬅️ Retour aux abonnements"):
    st.session_state["go_back"] = True
    st.session_state["abo_id"] = None
    st.session_state["scroll_top"] = True
    st.rerun()
