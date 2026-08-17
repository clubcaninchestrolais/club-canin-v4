import streamlit as st

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

# 📝 Procédures détaillées

## ➕ Ajouter un membre
1. Aller dans **Membres**  
2. Cliquer sur **Ajouter un membre**  
3. Remplir les informations  
4. Enregistrer

## 🐶 Ajouter un chien
1. Aller dans **Chiens**  
2. Cliquer sur **Ajouter un chien**  
3. Choisir le propriétaire  
4. Enregistrer

## 📅 Créer une séance
1. Aller dans **Séances**  
2. Cliquer sur **Créer une séance**  
3. Choisir la date, le moniteur, le type  
4. Enregistrer

## 🐕➡️📅 Inscrire un chien à un cours
1. Aller dans **Inscriptions**  
2. Choisir le membre  
3. Choisir le chien  
4. Choisir la séance  
5. Enregistrer

## ✔️ Enregistrer une présence
1. Aller dans **Présences**  
2. Choisir la séance du jour  
3. Cocher les membres présents  
4. Enregistrer

---

# 🐾 Flux extérieur — Préinscription et liaison du chien

Le flux extérieur permet à un non‑membre de préinscrire son chien à une séance via la page publique.

Ce flux crée automatiquement :
- un **non_membre**  
- un **chien non lié** (membre_id = NULL)  
- une **préinscription**  

Après validation et transformation, le membre devient actif, mais **le chien n’est pas encore lié automatiquement**.  
Cette étape est volontaire : elle permet de vérifier que le chien correspond bien au bon membre.

---

## 🔗 Lier le chien au membre (méthode officielle)

La liaison se fait **manuellement** dans la fiche du chien.

### Étapes :
1. Aller dans **Chiens**  
2. Cliquer sur **Modifier**  
3. Sélectionner le chien concerné  
4. Choisir le membre dans le champ **Propriétaire / membre**  
5. Enregistrer

🎯 Cette méthode est simple, fiable et évite les erreurs de liaison automatique.

---

## 📌 Pourquoi cette liaison n’est pas automatique ?

- Le club préfère **valider manuellement** les informations extérieures  
- Certains chiens peuvent être associés à un autre membre que celui saisi dans la préinscription  
- Cela évite les erreurs de saisie ou les doublons  
- Cela garde un contrôle total sur les données du club

---

## 🐶 Résultat final

Une fois la liaison faite :
- le chien apparaît dans les inscriptions  
- il peut être inscrit aux séances  
- il peut être comptabilisé dans les présences  
- le flux extérieur est entièrement opérationnel

---

# 🧩 Questions fréquentes

### ❓ Je ne vois pas un chien dans la liste
➡ Le chien n’est pas lié à un membre  
➡ Le membre est inactif  
➡ Le chien n’a pas été créé

### ❓ Je ne peux pas enregistrer une présence
➡ Le membre n’est pas inscrit à la séance  
➡ La séance n’existe pas  
➡ La date est incorrecte

### ❓ Une séance n’apparaît pas dans les inscriptions
➡ Elle n’a pas été créée  
➡ Elle est dans un autre groupe  
➡ La date est passée

---

# 🧭 Navigation

- [Membres](ca://s?q=Ouvrir_page_membres)  
- [Chiens](ca://s?q=Ouvrir_page_chiens)  
- [Inscriptions](ca://s?q=Ouvrir_page_inscriptions)  
- [Présences](ca://s?q=Ouvrir_page_presences)  
- [Séances](ca://s?q=Ouvrir_page_seances)

---

# 💬 Conclusion

Cette page sert de **guide officiel** pour les utilisateurs du club.  
Elle explique clairement **comment fonctionne le système**,  
et **dans quel ordre** les actions doivent être réalisées.

Si tu veux, je peux aussi ajouter :
- un **schéma visuel du flux**  
- une **FAQ plus complète**  
- une **section “Erreurs courantes et solutions”**  
- une **version PDF imprimable**  
""")
