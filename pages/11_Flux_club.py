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

# 🐾 Flux extérieur — Mode d’emploi simple et fun pour préposé

Ce flux explique comment gérer un **non‑membre** qui arrive au club, participe à un cours,
et souhaite ensuite devenir membre.  
Cette version est volontairement **simple**, **visuelle** et **préposé‑proof**.

---

## 🟢 1. L’extérieur arrive (préinscription publique)

L’accueil encode :
- Nom du visiteur  
- Nom du chien  
- Cours choisi  
- Séance du jour  

Cela crée automatiquement :
- un **membre temporaire**  
- un **chien temporaire**  
- une **préinscription**

➡ *L’extérieur existe maintenant dans le système.*

---

## 🔵 2. Avant le cours : valider la préinscription

Page : **Validation des préinscriptions**  
👉 Cliquer sur **Valider**

Effets automatiques :
- La **présence du jour** est créée  
- Le chien temporaire est lié  
- L’extérieur apparaît dans **Présences du jour**

➡ *Il est prêt pour le cours.*

---

## 🟠 3. Pendant le cours : valider la présence

Page : **Présences du jour**  
👉 Cocher **Présent** ou **Absent**

➡ *La présence est enregistrée dans l’historique.*

---

## 🟡 4. Après le cours : l’extérieur veut devenir membre

Menu : **Transformer en membre**

Effets automatiques :
- Cotisation créée  
- Abonnement créé  
- Statut membre activé dans la base

➡ *Administrativement, il est membre.*

---

## 🟣 5. Dernière étape : confirmer l’affiliation

Fiche du membre  
👉 Cliquer sur **Confirmation affiliation**

Effets :
- Le badge rouge **TEMPORAIRE** disparaît  
- Le membre devient officiel  
- Le chien devient officiel  
- Le bouton disparaît

➡ *La boucle est bouclée.*

---

# 🟩 Résumé SUPER SIMPLE

1️⃣ Préinscription  
2️⃣ Valider préinscription  
3️⃣ Valider présence  
4️⃣ Transformer en membre  
5️⃣ Confirmer affiliation  

➡ Si tu vois **TEMPORAIRE** → il reste l’étape 5.  
➡ Si **TEMPORAIRE a disparu** → flux terminé.

---

# 🎨 Version ULTRA FUN (style panneau mural)

🟢 ARRIVÉE EXTÉRIEUR  
↓  
🔵 VALIDER PRÉINSCRIPTION  
↓  
🟠 VALIDER PRÉSENCE  
↓  
🟡 TRANSFORMER EN MEMBRE  
↓  
🟣 CONFIRMER AFFILIATION  
↓  
🎉 FINI !


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
