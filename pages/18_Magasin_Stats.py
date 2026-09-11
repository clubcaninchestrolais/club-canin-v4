import streamlit as st
from securite import securite_user
securite_user()
import pandas as pd

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Statistiques", page_icon="📊", layout="wide")

# --- MASQUER LE MENU AUTOMATIQUE ---
hide_streamlit_menu()

# --- AFFICHER LE MENU PERSONNALISÉ ---
menu_lateral()

st.title("📊 Statistiques magasin du club")

# ---------------------------------------------------------
# TON CODE STATISTIQUES EXISTANT ICI
# ---------------------------------------------------------

# Exemple :
# st.subheader("Fréquentation des cours")
# ...


# ---------------------------------------------------------
# Charger les données
# ---------------------------------------------------------
def charger_produits():
    return supabase.table("produits").select("*").execute().data

def charger_achats():
    return supabase.table("achats_magasin").select("*").execute().data

def charger_ventes():
    return supabase.table("ventes_magasin").select("*").execute().data

produits = charger_produits()
achats = charger_achats()
ventes = charger_ventes()

if not produits:
    st.warning("Aucun produit enregistré.")
    st.stop()

# ---------------------------------------------------------
# Calculs
# ---------------------------------------------------------
df_produits = pd.DataFrame(produits)
df_achats = pd.DataFrame(achats) if achats else pd.DataFrame()
df_ventes = pd.DataFrame(ventes) if ventes else pd.DataFrame()

# Valeur du stock
df_produits["valeur_stock"] = df_produits["stock"] * df_produits["prix_achat"]
valeur_stock_totale = df_produits["valeur_stock"].sum()

# Bénéfice total
benefice_total = 0

if not df_ventes.empty:
    for _, vente in df_ventes.iterrows():
        produit = df_produits[df_produits["id"] == vente["produit_id"]].iloc[0]
        benefice_total += (vente["prix_vente_unitaire"] - produit["prix_achat"]) * vente["quantite"]

# ---------------------------------------------------------
# Affichage des indicateurs
# ---------------------------------------------------------
st.subheader("📌 Indicateurs principaux")

col1, col2 = st.columns(2)

with col1:
    st.metric("Valeur totale du stock", f"{valeur_stock_totale:.2f} €")

with col2:
    st.metric("Bénéfice total réalisé", f"{benefice_total:.2f} €")

# ---------------------------------------------------------
# Détail par produit
# ---------------------------------------------------------
st.subheader("📦 Détail par produit")

for _, p in df_produits.iterrows():
    # Calcul du bénéfice par produit
    benefice_produit = 0
    if not df_ventes.empty:
        ventes_p = df_ventes[df_ventes["produit_id"] == p["id"]]
        for _, v in ventes_p.iterrows():
            benefice_produit += (v["prix_vente_unitaire"] - p["prix_achat"]) * v["quantite"]

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
        Valeur du stock : {p['valeur_stock']:.2f} €<br>
        Bénéfice réalisé : <b>{benefice_produit:.2f} €</b>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Historique des achats
# ---------------------------------------------------------
st.subheader("📥 Historique des achats")

if df_achats.empty:
    st.info("Aucun achat enregistré.")
else:
    st.dataframe(df_achats)

# ---------------------------------------------------------
# Historique des ventes
# ---------------------------------------------------------
st.subheader("💰 Historique des ventes")

if df_ventes.empty:
    st.info("Aucune vente enregistrée.")
else:
    st.dataframe(df_ventes)
