import streamlit as st

# ------------------------------------------------------------
# PDF sans librairie externe (méthode 100% compatible Streamlit Cloud)
# ------------------------------------------------------------

documentation = """
DOCUMENTATION TECHNIQUE — CLUB CANIN CHESTROLAIS

1. INTRODUCTION
- Mission du club
- Objectifs du système numérique
- Architecture générale (Streamlit + Supabase)
- Rôles : membre, préposé, comité

2. FLUX EXTÉRIEUR
- Préinscription : public_portail.py → table preinscriptions
- Validation : page_60_validation.py → Accepté/Refusé
- Transformation : page_70_transformation.py → membres, chiens, cotisations, abonnements
- Nettoyage automatique : trigger delete_preinscriptions()

3. FLUX MEMBRE
- Connexion : login.py → Auth Supabase
- Inscription : page_80_inscription.py → table presences
- Présence : page_90_presence.py
- Décrémentation : trigger update_abonnement()
- Historique : page_100_historique.py → table historique

4. SCHÉMAS OFFICIELS
- Schéma global corporate
- Schéma technique
- Schéma vertical membre
- Schéma horizontal global
- Schéma extérieur

5. SÉCURITÉ & RLS SUPABASE
- RLS membres, chiens, presences, preinscriptions, abonnements, historique

6. ARCHITECTURE TECHNIQUE
- Structure des pages Streamlit
- Structure des tables Supabase
- Triggers et fonctions automatiques

7. ANNEXES
- Glossaire
- Codes d’erreurs
- Procédures internes
- Contacts du comité
"""

st.title("📘 Documentation du Club — Export PDF")

st.download_button(
    label="📄 Télécharger la documentation complète (PDF)",
    data=documentation.encode("utf-8"),
    file_name="documentation_club.pdf",
    mime="application/pdf"
)
