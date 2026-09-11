import streamlit as st
from supabase_rest import supabase, log_action   # ⭐ Import correct

st.set_page_config(page_title="Magasin – Ventes", page_icon="💰")

st.title("💰 Vente de produits du magasin")
from menu_lateral import menu_lateral
menu_lateral()

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
# Charger les membres
# ---------------------------------------------------------
def charger_membres():
    return (
        supabase.table("membres")
        .select("id, nom, prenom")
        .order("nom", desc=False)
        .execute()
        .data
    )

produits = charger_produits()
membres = charger_membres()

if not produits:
    st.warning("Aucun produit disponible.")
    st.stop()

if not membres:
    st.warning("Aucun membre enregistré.")
    st.stop()

# ---------------------------------------------------------
# Formulaire de vente
# ---------------------------------------------------------
st.subheader("➖ Enregistrer une vente")

with st.form("form_vente"):
    noms_produits = {p["nom"]: p for p in produits}
    choix_nom = st.selectbox("Produit vendu", list(noms_produits.keys()))
    produit = noms_produits[choix_nom]

    noms_membres = {f"{m['prenom']} {m['nom']}": m for m in membres}
    choix_membre = st.selectbox("Membre acheteur", list(noms_membres.keys()))
    membre = noms_membres[choix_membre]

    quantite = st.number_input("Quantité vendue", min_value=1, step=1)

    prix_vente_unitaire = st.number_input(
        "Prix de vente unitaire (€)",
        min_value=0.0,
        step=0.1,
        value=float(produit["prix_vente"])
    )

    submitted = st.form_submit_button("Enregistrer la vente")

    if submitted:
        # Vérification du stock
        if quantite > produit["stock"]:
            st.error(f"Stock insuffisant ! Stock actuel : {produit['stock']}")
            st.stop()

        # Enregistrer la vente
        supabase.table("ventes_magasin").insert({
            "produit_id": produit["id"],
            "quantite": quantite,
            "prix_vente_unitaire": prix_vente_unitaire,
            "id_membre": membre["id"]
        }).execute()

        # Mise à jour du stock
        nouveau_stock = produit["stock"] - quantite

        supabase.table("produits").update({
            "stock": nouveau_stock
        }).eq("id", produit["id"]).execute()

        # ⭐ Journal des actions
        log_action(
            "Vente magasin",
            f"Produit : {produit['nom']} | Quantité : {quantite} | Prix vente : {prix_vente_unitaire} € | Membre : {choix_membre} | Utilisateur : {st.session_state.get('username')}"
        )

        st.success(f"Vente enregistrée. Nouveau stock de {produit['nom']} : {nouveau_stock}")
