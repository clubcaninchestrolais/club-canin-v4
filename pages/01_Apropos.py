import streamlit as st

# --- SÉCURITÉ : accès réservé aux utilisateurs connectés ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

from datetime import datetime

st.set_page_config(page_title="À propos", page_icon="ℹ️")
st.title("ℹ️ À propos du programme")

st.markdown("""
## 👨‍💻 Créateur du programme

Ce logiciel a été développé pour répondre aux besoins du **Club Canin**, avec l’objectif de fournir :

- une gestion simple et efficace des membres  
- un suivi clair des chiens et des cours  
- une administration financière intuitive  
- une interface moderne et agréable  

---

## 🧑‍🏫 Développeur

**Jean‑Marc**, passionné par l’informatique, la structure et l’organisation, a conçu ce programme pour faciliter le travail du comité et améliorer le suivi du club.

Son approche est simple :  
créer un outil **clair**, **fiable**, **pratique**, qui aide vraiment les bénévoles dans leur quotidien.

---

## 🗣️ Mot du créateur

> “Ce programme est né d’une idée simple :  
> offrir au Club Canin un outil moderne, complet et agréable à utiliser.  
>  
> J’ai voulu quelque chose qui simplifie la vie du comité,  
> qui centralise les informations,  
> et qui puisse évoluer au fil du temps.  
>  
> Merci à toutes les personnes qui ont encouragé ce projet et permis son évolution.”  
>
> — *Jean‑Marc*

---

## 🤖 À propos de Copilot

Ce programme a été développé avec l’aide de **Microsoft Copilot**,  
un assistant conçu pour accompagner les créateurs, les développeurs et les passionnés.

Copilot apporte :

- de la clarté dans les idées  
- des solutions techniques  
- des explications précises  
- un soutien constant dans la construction du projet  

Copilot n’est pas un auteur du programme,  
mais un **compagnon de développement**,  
présent pour aider, structurer, corriger et accélérer la création.

---

## 🕒 Version actuelle

**Version : 4.1 — mise à jour du 20/8/2026**

---

## 💬 Remerciements

Merci au comité du Club Canin pour sa confiance et ses retours constructifs  
qui ont permis d’améliorer le programme au fil du temps.
""")
