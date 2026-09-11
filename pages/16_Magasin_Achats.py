import streamlit as st
from supabase_rest import supabase

# ⭐ Import propre du journal des actions
import pages.Audit_Log_90 as audit
log_action = audit.log_action

st.set_page_config(page_title="Magasin – Achats", page_icon="📥")

st.title("📥 Réapprovisionnement du magasin")

def charger_produits():
    return (
        supabase.table("produits")
        .select("*")
        .order("nom", desc=False)
        .execute()
        .data
    )

produits = charger_produits()

if not produits:
    st.warning("Aucun produit disponible. Ajoutez d'abord des produits.")
    st.stop()

st.subheader("➕ Ajouter un achat (réapprovisionnement)")

with st.form("form_achat"):
    noms = {p["nom"]: p for p in produits}
    choix_nom = st.selectbox("Produit", list(noms.keys()))
    produit = noms[choix_nom]

    quantite = st.number_input("Quantité achetée", min_value=1, step=1)
    prix_achat_unitaire = st.number_input("Prix d'achat unitaire (€)", min_value=0.0, step=0.1)
    fournisseur = st.text_input("Fournisseur (optionnel)")

    submitted = st.form_submit_button("Enregistrer l'achat")

    if submitted:
        supabase.table("achats_magasin").insert({
            "produit_id": produit["id"],
            "quantite": quantite,
            "prix_achat_unitaire": prix_achat_unitaire,
            "fournisseur": fournisseur
        }).execute()

        nouveau_stock = produit["stock"] + quantite

        supabase.table("produits").update({
            "stock": nouveau_stock
        }).eq("id", produit["id"]).execute()

        log_action(
            "Achat magasin",
            f"Produit : {produit['nom']} | Quantité : {quantite} | Prix achat : {prix_achat_unitaire} € | Utilisateur : {st.session_state.get('username')}"
        )

        st.success(f"Achat enregistré. Nouveau stock de {produit['nom']} : {nouveau_stock}")
