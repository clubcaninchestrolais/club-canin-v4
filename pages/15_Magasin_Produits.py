import streamlit as st
from securite import securite_user
securite_user()

from supabase_rest import supabase, log_action
from menu import hide_streamlit_menu, menu_lateral

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Produits du magasin", page_icon="📦", layout="wide")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("📦 Gestion des produits du magasin")

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
    st.warning("Aucun produit enregistré.")
    st.stop()

# ---------------------------------------------------------
# Affichage des produits
# ---------------------------------------------------------
st.subheader("📦 Liste des produits")

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

# ---------------------------------------------------------
# Ajouter un produit
# ---------------------------------------------------------
st.subheader("➕ Ajouter un produit")

with st.form("form_produit"):
    nom = st.text_input("Nom du produit")
    categorie = st.text_input("Catégorie")
    prix_achat = st.number_input("Prix d'achat (€)", min_value=0.0, step=0.1)
    prix_vente = st.number_input("Prix de vente (€)", min_value=0.0, step=0.1)
    stock_initial = st.number_input("Stock initial", min_value=0, step=1)

    submitted = st.form_submit_button("Ajouter")

    if submitted:
        if not nom:
            st.error("Le nom du produit est obligatoire.")
            st.stop()

        supabase.table("produits").insert({
            "nom": nom,
            "categorie": categorie,
            "prix_achat": prix_achat,
            "prix_vente": prix_vente,
            "stock": stock_initial
        }).execute()

        log_action(
            "Ajout produit",
            f"Produit : {nom} | Catégorie : {categorie} | Stock initial : {stock_initial} | Utilisateur : {st.session_state.get('username')}"
        )

        st.success(f"Produit {nom} ajouté avec succès.")
        st.rerun()
# ---------------------------------------------------------
# Modifier un produit existant
# ---------------------------------------------------------
st.subheader("✏️ Modifier un produit")

# Liste des produits par nom
noms_produits = {p["nom"]: p for p in produits}
choix_modif = st.selectbox("Sélectionner un produit à modifier", list(noms_produits.keys()))

produit_modif = noms_produits[choix_modif]

with st.form("form_modif_produit"):
    nom = st.text_input("Nom du produit", value=produit_modif["nom"])
    categorie = st.text_input("Catégorie", value=produit_modif["categorie"])
    prix_achat = st.number_input("Prix d'achat (€)", min_value=0.0, step=0.1, value=float(produit_modif["prix_achat"]))
    prix_vente = st.number_input("Prix de vente (€)", min_value=0.0, step=0.1, value=float(produit_modif["prix_vente"]))
    stock = st.number_input("Stock actuel", min_value=0, step=1, value=int(produit_modif["stock"]))

    submitted_modif = st.form_submit_button("Enregistrer les modifications")

    if submitted_modif:
        supabase.table("produits").update({
            "nom": nom,
            "categorie": categorie,
            "prix_achat": prix_achat,
            "prix_vente": prix_vente,
            "stock": stock
        }).eq("id", produit_modif["id"]).execute()

        log_action(
            "Modification produit",
            f"Produit modifié : {nom} | Catégorie : {categorie} | Stock : {stock} | Utilisateur : {st.session_state.get('username')}"
        )

        st.success(f"Produit {nom} modifié avec succès.")
        st.rerun()
