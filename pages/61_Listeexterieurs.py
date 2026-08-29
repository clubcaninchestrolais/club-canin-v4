import streamlit as st
from supabase import create_client, Client
from datetime import datetime, timedelta
from menu import hide_streamlit_menu, menu_lateral

hide_streamlit_menu()
menu_lateral()

# --- Connexion Supabase ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("📋 Liste des extérieurs (préinscriptions)")

# ---------------------------------------------------------
# 🧹 NETTOYAGE AUTOMATIQUE DES PREINSCRIPTIONS
# ---------------------------------------------------------

limite = datetime.now() - timedelta(days=30)

# 1️⃣ Supprimer les refusés
supabase.table("preinscriptions").delete().eq("acceptee", False).execute()

# 2️⃣ Supprimer les transformés
supabase.table("preinscriptions").delete().eq("statut", "transforme").execute()

# 3️⃣ Supprimer les anciennes préinscriptions (> 30 jours)
supabase.table("preinscriptions").delete().lt("created_at", limite.isoformat()).execute()

# ---------------------------------------------------------
# Charger les extérieurs encore actifs
# ---------------------------------------------------------

preins = (
    supabase.table("preinscriptions")
    .select("*")
    .eq("type", "exterieur")
    .execute()
    .data
)

if not preins:
    st.info("Aucun extérieur actif.")
    st.stop()

# ---------------------------------------------------------
# Affichage
# ---------------------------------------------------------

for p in preins:
    st.markdown("---")
    st.write(f"👤 **{p['prenom']} {p['nom']}**")
    st.write(f"📧 {p['email']}")
    st.write(f"📱 {p['telephone']}")
    st.write(f"🐶 {p['chien_nom']} ({p['chien_race']})")
    st.write(f"🆔 ID préinscription : {p['id']}")
    st.write(f"📌 Statut : **{p['statut']}**")
