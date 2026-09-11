import streamlit as st
from supabase_rest import supabase

st.set_page_config(page_title="Magasin – Produits", page_icon="🛒")

st.title("🛒 Gestion des produits du magasin")

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

# ---------------------------------------------------------
# Ajouter un produit
# ---------------------------------------------------------
st.subheader("➕ Ajouter un produit")

with st.form("ajout_produit"):
    nom = st.text_input("Nom du produit")
    categorie = st.text_input("Catégorie")
    prix_achat = st.number_input("Prix d'achat unitaire (€)", min_value=0.0, step=0.1)
    prix_vente = st.number_input("Prix de vente unitaire (€)", min_value=0.0, step=0.1)
    stock = st.number_input("Stock initial", min_value=0, step=1)

    submitted = st.form_submit_button("Ajouter")

    if submitted:
        supabase.table("produits").insert({
            "nom": nom,
            "categorie": categorie,
            "prix_achat": prix_achat,
            "prix_vente": prix_vente,
            "stock": stock
        }).execute()

        st.success(f"Produit '{nom}' ajouté avec succès.")

# ---------------------------------------------------------
# Liste des produits
# ---------------------------------------------------------
st.subheader("📦 Liste des produits")

produits = charger_produits()

if not produits:
    st.info("Aucun produit enregistré pour le moment.")
else:
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
            Prix d'achat : {p['prix_achat']} €<br>
            Prix de vente : {p['prix_vente']} €<br>
            Stock actuel : <b>{p['stock']}</b>
        </div>
        """, unsafe_allow_html=True)
