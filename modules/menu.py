import streamlit as st

def afficher_menu():
    with st.sidebar:
        st.markdown("### 🟦 Gestion quotidienne")
        st.page_link("pages/1_Membres.py", label="👥 Membres")
        st.page_link("pages/2_Chiens.py", label="🐶 Chiens")
        st.page_link("pages/3_Presences.py", label="📋 Présences")
        st.page_link("pages/12_Validation_Presence.py", label="✔️ Validation présence")
        st.page_link("pages/11_Inscription.py", label="📝 Inscription")
        st.page_link("pages/10_Activites_speciales.py", label="⭐ Activités spéciales")

        st.markdown("### 🟧 Administration")
        st.page_link("pages/5_Cotisations.py", label="💶 Cotisations")
        st.page_link("pages/09_Abonnements.py", label="📅 Abonnements")
        st.page_link("pages/6_Finances.py", label="📊 Finances")
        st.page_link("pages/4_Cours.py", label="🎓 Cours")
        st.page_link("pages/7_Statistiques.py", label="📈 Statistiques")

        st.markdown("### 🟩 Technique")
        st.page_link("pages/8_Parametres.py", label="⚙️ Paramètres")
        st.page_link("pages/13_A_Propos.py", label="ℹ️ À propos")
        st.page_link("pages/14_Deconnexion.py", label="🚪 Déconnexion")
