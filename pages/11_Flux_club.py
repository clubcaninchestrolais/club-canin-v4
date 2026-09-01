import streamlit as st

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from menu import hide_streamlit_menu, menu_lateral

st.set_page_config(page_title="Aide — Flux du club", page_icon="❓")

hide_streamlit_menu()
menu_lateral()

st.title("❓ Aide — Comprendre les flux du club")

# ---------------------------------------------------------
# Texte segmenté pour éviter les erreurs de syntaxe
# ---------------------------------------------------------

st.markdown("## 🐕 Pourquoi cette page ?")
st.markdown(
    "Cette page explique le fonctionnement réel du système du club, "
    "tel qu’il est aujourd’hui dans l’application : flux extérieur, flux membre, "
    "validation, transformation, présence, décrémentation, sécurité et logique des pages."
)

st.markdown("---")
st.markdown("# 🔄 Vue d’ensemble des flux du club")

st.markdown("### 🟧 Flux extérieur (nouveau visiteur)")
st.markdown(
    "1. Préinscription extérieure\n"
    "2. Validation (page 60)\n"
    "3. Transformation en membre (page 70)\n"
    "4. Création automatique du chien\n"
    "5. Nettoyage automatique"
)

st.markdown("### 🟦 Flux membre (membres du club)")
st.markdown(
    "1. Connexion membre\n"
    "2. Inscription à une séance\n"
    "3. Présence\n"
    "4. Décrémentation automatique de l’abonnement\n"
    "5. Historique complet"
)

st.markdown("---")
st.markdown("## 🟧 Flux extérieur — fonctionnement complet")

st.markdown("### 1️⃣ Préinscription extérieure")
st.markdown(
    "Un non‑membre remplit un formulaire public. "
    "Cela crée une préinscription dans la base."
)

st.markdown("### 2️⃣ Validation (page 60)")
st.markdown(
    "Le préposé accepte ou refuse la préinscription.\n\n"
    "✔ Accepté → passe en transformation\n"
    "❌ Refusé → supprimé automatiquement"
)

st.markdown("### 3️⃣ Transformation (page 70)")
st.markdown(
    "La transformation crée automatiquement :\n"
    "- un membre\n"
    "- un chien lié au membre\n"
    "- une cotisation\n"
    "- un abonnement\n\n"
    "La préinscription est ensuite archivée."
)

st.markdown("### 4️⃣ Nettoyage automatique")
st.markdown(
    "Les préinscriptions refusées ou transformées sont supprimées automatiquement "
    "pour éviter la pollution Facebook."
)

st.markdown("---")
st.markdown("## 🟦 Flux membre — fonctionnement complet")

st.markdown("### 1️⃣ Connexion membre")
st.markdown(
    "Le membre se connecte avec son email et son mot de passe. "
    "Il accède à son espace personnel."
)

st.markdown("### 2️⃣ Inscription à une séance")
st.markdown(
    "Le membre choisit une séance disponible. "
    "Une inscription est créée dans la base."
)

st.markdown("### 3️⃣ Présence")
st.markdown(
    "Le jour du cours, le préposé enregistre la présence. "
    "Chaque présence crée une ligne dans l’historique."
)

st.markdown("### 4️⃣ Décrémentation automatique")
st.markdown(
    "Si le membre est présent, son abonnement est décrémenté automatiquement. "
    "Le nouveau solde est mis à jour dans la base."
)

st.markdown("### 5️⃣ Historique")
st.markdown(
    "Toutes les actions (inscriptions, présences, absences, décrémentations) "
    "sont enregistrées dans l’historique du membre."
)

st.markdown("---")
st.markdown("## 🔐 Sécurité et rôles")

st.markdown(
    "Toutes les pages sont protégées par un contrôle de session. "
    "Les rôles (admin / user) limitent l’accès aux pages sensibles."
)

st.markdown("---")
st.markdown("## 🧭 Résumé final")

st.markdown("### 🟧 Flux extérieur")
st.markdown(
    "1. Préinscription\n"
    "2. Validation\n"
    "3. Transformation\n"
    "4. Membre + chien\n"
    "5. Nettoyage automatique"
)

st.markdown("### 🟦 Flux membre")
st.markdown(
    "1. Connexion\n"
    "2. Inscription\n"
    "3. Présence\n"
    "4. Décrémentation\n"
    "5. Historique"
)

