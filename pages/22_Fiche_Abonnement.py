import streamlit as st
from supabase_rest import supabase
from datetime import datetime

st.set_page_config(page_title="Fiche Abonnement", page_icon="📄")
st.title("📄 Détail de l'abonnement")

# ---------------------------------------------------------
# 1. Vérifier que l’ID est présent
# ---------------------------------------------------------
if "abo_id" not in st.session_state:
    st.error("Aucun abonnement sélectionné.")
    st.stop()

abo_id = st.session_state["abo_id"]

# ---------------------------------------------------------
# 2. Charger l’abonnement
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
# 3. Charger le membre lié
# ---------------------------------------------------------
membre = (
    supabase.table("membres")
    .select("*")
    .eq("id", abo["membre_id"])
    .execute()
    .data[0]
)

# ---------------------------------------------------------
# 4. Affichage des informations
# ---------------------------------------------------------
st.subheader("👤 Informations du membre")
st.write(f"**Nom :** {membre['nom']}")
st.write(f"**Prénom :** {membre['prenom']}")
st.write(f"**Statut :** {membre['statut']}")

st.markdown("---")

st.subheader("🎫 Informations de l'abonnement")
st.write(f"**ID abonnement :** {abo['id']}")
st.write(f"**Total séances :** {abo['seances_total']}")
st.write(f"**Séances restantes :** {abo['seances_restantes']}")
st.write(f"**Prix :** {abo['prix']} €")
st.write(f"**Date d'achat :** {abo['date_achat']}")
st.write(f"**Actif :** {'Oui' if abo['actif'] else 'Non'}")

st.markdown("---")

# ---------------------------------------------------------
# 5. Boutons +1 / -1
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
# 6. Désactivation / activation de l’abonnement
# ---------------------------------------------------------
if abo["actif"]:
    if st.button("🔴 Désactiver l'abonnement"):
        supabase.table("abonnements").update({
            "actif": False
        }).eq("id", abo_id).execute()
        st.success("Abonnement désactivé.")
        st.rerun()
else:
    if st.button("🟢 Réactiver l'abonnement"):
        supabase.table("abonnements").update({
            "actif": True
        }).eq("id", abo_id).execute()
        st.success("Abonnement réactivé.")
        st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# 7. Retour
# ---------------------------------------------------------
if st.button("⬅️ Retour aux abonnements"):
    st.switch_page("pages/21_Abonnements.py")
