import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from menu import hide_streamlit_menu, menu_lateral

st.set_page_config(page_title="Aide — Flux du club", page_icon="❓")

hide_streamlit_menu()
menu_lateral()

st.title("❓ Aide — Comprendre les flux du club")

st.markdown("""
## 🐕 Pourquoi cette page ?

Cette page explique **le fonctionnement réel du système du club**,  
tel qu’il est aujourd’hui dans l’application :  
flux intérieur, flux extérieur, validation, transformation, sécurité, et logique des pages.

Elle sert de guide officiel pour les utilisateurs du comité.

---

# 🔄 Vue d’ensemble des flux du club

Le club fonctionne avec **2 flux principaux** :

### 🟦 Flux intérieur (membres du club)
1. **Membres**
2. **Chiens**
3. **Séances**
4. **Inscriptions**
5. **Présences**

### 🟧 Flux extérieur (préinscriptions via Facebook)
1. **Préinscription extérieure**
2. **Validation (accepter / refuser)**
3. **Transformation en membre**
4. **Création automatique du chien**
5. **Fin du flux extérieur**

Les deux flux sont **séparés**, mais se rejoignent lorsque l’extérieur devient membre.

---

# 🟦 Flux intérieur — fonctionnement complet

## 1️⃣ Membres
Un membre doit être créé en premier.

Un membre contient :
- Nom
- Adresse
- Contact
- Statut (actif / inactif)

Sans membre → impossible d’ajouter un chien.

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

## 3️⃣ Séances
Les séances sont créées par le club.

Une séance contient :
- Date
- Moniteur
- Type de cours
- Groupe

Sans séance → impossible d’inscrire un membre.

---

## 4️⃣ Inscriptions
Une inscription = **membre + chien + séance**

Elle permet :
- de réserver la place
- de préparer la liste des participants

Sans inscription → impossible d’enregistrer une présence.

---

## 5️⃣ Présences
La présence est enregistrée **le jour du cours**.

Elle permet :
- de comptabiliser la participation
- de suivre l’assiduité
- de générer les statistiques

---

# 🟧 Flux extérieur — fonctionnement complet

## 1️⃣ Préinscription extérieure
Un non‑membre remplit un formulaire public (Facebook).

Cela crée :
- un **non_membre**
- un **chien non lié**
- une **préinscription**

---

## 2️⃣ Validation
Le préposé valide ou refuse.

### ✔ Si accepté :
- `traitee = True`
- `acceptee = True`
- `statut = "valide"`
- La préinscription apparaît dans **Transformation**

### ❌ Si refusé :
- `traitee = True`
- `acceptee = False`
- `statut = "archive"`
- La préinscription est **supprimée automatiquement** (nettoyage)

---

## 3️⃣ Transformation
Si accepté, le préposé transforme l’extérieur en membre.

La transformation :
- crée un **membre**
- crée un **chien lié**
- archive la préinscription
- supprime les données extérieures inutiles

---

## 4️⃣ Nettoyage automatique
Chaque chargement de la page 61 supprime :
- les refusés
- les transformés
- les préinscriptions inutiles

Le flux extérieur reste propre.

---

# 🔐 Sécurité et rôles

L’accès aux pages est protégé par :

```python
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

