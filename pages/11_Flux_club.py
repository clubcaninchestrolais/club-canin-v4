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
    "tel qu’il est aujourd’hui dans l’application : flux intérieur, flux extérieur, "
    "validation, transformation, sécurité, et logique des pages."
)

st.markdown("---")
st.markdown("# 🔄 Vue d’ensemble des flux du club")

st.markdown("### 🟦 Flux intérieur (membres du club)")
st.markdown("1. Membres\n2. Chiens\n3. Séances\n4. Inscriptions\n5. Présences")

st.markdown("### 🟧 Flux extérieur (préinscriptions via Facebook)")
st.markdown("1. Préinscription\n2. Validation\n3. Transformation\n4. Membre + chien\n5. Nettoyage automatique")

st.markdown("---")
st.markdown("## 🟦 Flux intérieur — fonctionnement complet")

st.markdown("### 1️⃣ Membres")
st.markdown(
    "Un membre doit être créé en premier. "
    "Sans membre → impossible d’ajouter un chien."
)

st.markdown("### 2️⃣ Chiens")
st.markdown(
    "Chaque chien est lié à un membre. "
    "Sans chien → impossible d’inscrire à une séance."
)

st.markdown("### 3️⃣ Séances")
st.markdown(
    "Les séances sont créées par le club. "
    "Sans séance → impossible d’inscrire un membre."
)

st.markdown("### 4️⃣ Inscriptions")
st.markdown(
    "Une inscription = membre + chien + séance. "
    "Sans inscription → impossible d’enregistrer une présence."
)

st.markdown("### 5️⃣ Présences")
st.markdown(
    "La présence est enregistrée le jour du cours. "
    "Elle permet de suivre l’assiduité et les statistiques."
)

st.markdown("---")
st.markdown("## 🟧 Flux extérieur — fonctionnement complet")

st.markdown("### 1️⃣ Préinscription extérieure")
st.markdown(
    "Un non‑membre remplit un formulaire public. "
    "Cela crée une préinscription."
)

st.markdown("### 2️⃣ Validation")
st.markdown(
    "Le préposé accepte ou refuse.\n\n"
    "✔ Accepté → transformation possible\n"
    "❌ Refusé → supprimé automatiquement"
)

st.markdown("### 3️⃣ Transformation")
st.markdown(
    "La transformation crée un membre + un chien, "
    "et archive la préinscription."
)

st.markdown("### 4️⃣ Nettoyage automatique")
st.markdown(
    "Les refusés et transformés sont supprimés automatiquement "
    "pour éviter la pollution Facebook."
)

st.markdown("---")
st.markdown("## 🔐 Sécurité et rôles")

st.markdown(
    "Toutes les pages sont protégées par un contrôle de session. "
    "Les rôles permettent de limiter l’accès aux pages sensibles."
)

st.markdown("---")
st.markdown("## 🧭 Résumé final")

st.markdown("### 🟦 Flux intérieur")
st.markdown("1. Membre\n2. Chien\n3. Séance\n4. Inscription\n5. Présence")

st.markdown("### 🟧 Flux extérieur")
st.markdown("1. Préinscription\n2. Validation\n3. Transformation\n4. Membre + chien\n5. Nettoyage automatique")
