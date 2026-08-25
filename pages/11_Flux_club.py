import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="Aide — Flux du club", page_icon="❓")
st.title("❓ Aide — Comprendre les flux du club")

st.markdown("""
## 🐕 Pourquoi cette page ?

Cette page explique **comment fonctionne le système du club**,  
et **dans quel ordre** les actions doivent être réalisées pour éviter les erreurs.

Elle sert de guide pour les utilisateurs du comité.

---

# 🔄 Les flux du club : vue d’ensemble

Le fonctionnement du club repose sur **5 flux principaux** :

1. **Membres**  
2. **Chiens**  
3. **Séances (cours)**  
4. **Inscriptions aux cours**  
5. **Présences aux cours**

Chaque flux dépend du précédent.  
Voici la logique :

---

## 1️⃣ Membres

Un membre doit être **créé en premier**.

Un membre contient :
- Nom  
- Adresse  
- Contact  
- Statut (actif / inactif)

Sans membre → impossible d’inscrire un chien ou un cours.

---

## 2️⃣ Chiens

Chaque chien doit être **lié à un membre**.

Un chien contient :
- Nom  
- Race  
- Date de naissance  
- Propriétaire (membre)

Sans chien → impossible d’inscrire à une séance.

---

## 3️⃣ Séances (cours)

Les séances sont créées par le club.

Une séance contient :
- Date  
- Moniteur  
- Type de cours  
- Groupe

Sans séance → impossible d’inscrire un membre.

---

## 4️⃣ Inscriptions aux cours

Une inscription signifie :  
👉 *un membre + un chien + une séance*

L’inscription permet :
- de réserver la place  
- de préparer la liste des participants  
- de suivre l’activité du club

Sans inscription → la présence ne peut pas être enregistrée.

---

## 5️⃣ Présences aux cours

La présence est enregistrée **le jour du cours**.

Elle permet :
- de comptabiliser la participation  
- de suivre l’assiduité  
- de générer les statistiques du club

---

# 🧭 Résumé du flux complet

Voici l’ordre **obligatoire** :

1️⃣ Créer un **membre**  
2️⃣ Ajouter un **chien**  
3️⃣ Créer une **séance**  
4️⃣ Faire une **inscription**  
5️⃣ Enregistrer la **présence**

Si un élément manque → l’action suivante ne fonctionne pas.

---

# 🐾 Flux extérieur — Mode d’emploi simple et fun pour préposé

(... contenu inchangé ...)
""")
