import streamlit as st
from securite import securite_admin
securite_admin()

from datetime import datetime
from supabase_rest import supabase

st.title("Rapport du Club – Vue d’ensemble")

st.write("Cette page présente un aperçu général des activités du club.")
st.write("Elle pourra être enrichie avec des graphiques, des statistiques et des analyses détaillées.")

# ---------------------------------------------------------
# Récupération des données
# ---------------------------------------------------------

# Nombre de membres
membres = supabase.table("membres").select("*").execute().data
nb_membres = len(membres)

# Nombre d'extérieurs
exterieurs = supabase.table("exterieurs").select("*").execute().data
nb_exterieurs = len(exterieurs)

# Cotisations actives
cotisations = supabase.table("cotisations").select("*").execute().data
nb_cotisations = len(cotisations)

# Abonnements actifs
abonnements = supabase.table("abonnements").select("*").execute().data
nb_abonnements = len(abonnements)

# ---------------------------------------------------------
# Affichage simple
# ---------------------------------------------------------

st.subheader("Résumé rapide")

col1, col2 = st.columns(2)

with col1:
    st.metric("Membres actifs", nb_membres)
    st.metric("Extérieurs enregistrés", nb_exterieurs)

with col2:
    st.metric("Cotisations actives", nb_cotisations)
    st.metric("Abonnements actifs", nb_abonnements)

st.info("Ce rapport est une version simple. Il pourra être enrichi avec des graphiques, des tendances, des comparaisons mensuelles, etc.")
