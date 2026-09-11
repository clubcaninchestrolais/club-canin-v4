import streamlit as st
from securite import securite_user
securite_user()

from supabase_rest import supabase, log_action
from menu import hide_streamlit_menu, menu_lateral

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Magasin – Achats", page_icon="📥", layout="wide")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("📥 Réapprovisionnement du magasin")

# ---------------------------------------------------------
# Charger les produits
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# Formulaire d'achat
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# Affichage du stock actuel
# ---------------------------------------------------------
st.subheader("📦 Stock actuel")

for p in produits:
    st.markdown(f"""
    <div style="
        padding: 12px;
        margin-bottom: 10px;
        border-radius: 10px;
        background-color: #f7f9fc;
        border: 1px solid #dce3f0;
    ">
        <b>{p['nom']}</b> — {p['categorie']}<br>
        Stock actuel : <b>{p['stock']}</b><br>
        Prix d'achat : {p['prix_achat']} €<br>
        Prix de vente : {p['prix_vente']} €
    </div>
    """, unsafe_allow_html=True)
