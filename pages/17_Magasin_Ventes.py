import streamlit as st
from securite import securite_user
securite_user()

from supabase_rest import supabase, log_action
from menu import hide_streamlit_menu, menu_lateral

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Magasin – Ventes", page_icon="💰", layout="wide")

hide_streamlit_menu()
menu_lateral()

st.title("💰 Vente de produits du magasin")

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

# ---------------------------------------------------------
# Gestion des cas où les tables sont vides
# ---------------------------------------------------------
if not produits:
    st.warning("Aucun produit disponible. Ajoutez d'abord des produits dans le magasin.")
    produits_disponibles = False
else:
    produits_disponibles = True

if not membres:
    st.warning("Aucun membre enregistré. Ajoutez d'abord des membres.")
    membres_disponibles = False
else:
    membres_disponibles = True

# ---------------------------------------------------------
# Formulaire de vente
# ---------------------------------------------------------
st.subheader("➖ Enregistrer une vente")

if produits_disponibles and membres_disponibles:

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
            if quantite > produit["stock"]:
                st.error(f"Stock insuffisant ! Stock actuel : {produit['stock']}")
                st.stop()

            supabase.table("ventes_magasin").insert({
                "produit_id": produit["id"],
                "quantite": quantite,
                "prix_vente_unitaire": prix_vente_unitaire,
                "id_membre": membre["id"]
            }).execute()

            nouveau_stock = produit["stock"] - quantite

            supabase.table("produits").update({
                "stock": nouveau_stock
            }).eq("id", produit["id"]).execute()

            log_action(
                "Vente magasin",
                f"Produit : {produit['nom']} | Quantité : {quantite} | Prix vente : {prix_vente_unitaire} € | Membre : {choix_membre} | Utilisateur : {st.session_state.get('username')}"
            )

            st.success(f"Vente enregistrée. Nouveau stock de {produit['nom']} : {nouveau_stock}")

else:
    st.info("Le formulaire de vente sera disponible lorsque des produits et des membres auront été ajoutés.")

# ---------------------------------------------------------
# Affichage du stock actuel
# ---------------------------------------------------------
st.subheader("📦 Stock actuel")

if produits_disponibles:
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
else:
    st.info("Aucun stock à afficher pour le moment.")
