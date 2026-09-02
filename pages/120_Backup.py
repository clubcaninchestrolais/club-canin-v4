import streamlit as st
import pandas as pd
import io
import zipfile
from supabase import create_client

# Connexion Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("💾 Backup des données du Club Canin")

st.write("Téléchargez une sauvegarde complète des tables du club.")

# Liste des tables à sauvegarder
tables = [
    "membres",
    "chiens",
    "cours",
    "cours_presences",
    "cours_seances",
    "cours_inscriptions",
    "cotisations",
    "abonnements",
    "finances_generales",
    "activites_speciales",
    "inscriptions_speciales",
    "historique"
]

zip_buffer = io.BytesIO()

with zipfile.ZipFile(zip_buffer, "w") as zip_file:
    for table in tables:
        try:
            response = supabase.table(table).select("*").execute()
            data = response.data

            if data is None:
                st.error(f"❌ Table vide ou introuvable : {table}")
                continue

            df = pd.DataFrame(data)
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            zip_file.writestr(f"{table}.csv", csv_bytes)

            st.success(f"✔ Table sauvegardée : {table}")

        except Exception:
            st.error(f"❌ Erreur lors de la lecture de la table : {table}")

# Bouton de téléchargement
st.download_button(
    label="📦 Télécharger le backup complet (ZIP)",
    data=zip_buffer.getvalue(),
    file_name="backup_club_canin.zip",
    mime="application/zip"
)

st.divider()

# --- Bouton pour afficher la procédure ---
if st.button("📘 Afficher la procédure Backup & Restore"):
    st.header("📘 Procédure Backup & Restore")

    st.subheader("💾 1) Procédure de Backup (Sauvegarde)")
    st.markdown("""
**Objectif :** créer une copie de sécurité de toutes les tables du club.

### 🟦 Étapes :
1. Ouvrir la page **Backup des données**.
2. Le programme teste chaque table :
   - 🟩 **Vert** : table sauvegardée  
   - 🟥 **Rouge** : table introuvable / vide / nom incorrect / RLS trop stricte
3. Cliquer sur **📦 Télécharger le backup complet (ZIP)**.
4. Le fichier ZIP est téléchargé sur votre ordinateur.
5. Le ZIP contient un fichier CSV par table (ex : `membres.csv`, `chiens.csv`, etc.).

### 🟨 Important :
- Le backup **n’est pas stocké dans Supabase**.  
- Le backup **n’est pas stocké dans Streamlit**.  
- Le backup **n’est pas stocké dans GitHub**.  
➡️ **Il est uniquement sur votre PC.**
""")

    st.subheader("🛠️ 2) Procédure de Restore (Restauration)")
    st.markdown("""
**Objectif :** réinjecter les données d’un fichier CSV dans une table Supabase.

---

### 🟥 A) Restaurer complètement une table
1. Aller dans **Supabase → SQL Editor**.
2. Vider la table :

3. Aller dans **Table Editor → Import → CSV**.
4. Choisir le fichier CSV correspondant (ex : `membres.csv`).
5. Valider.

➡️ Supabase recrée toutes les lignes proprement.

---

### 🟦 B) Restaurer partiellement une table
1. Aller dans **Table Editor → Import → CSV**.
2. Importer le fichier CSV **sans vider la table**.

➡️ Supabase ajoute les lignes et ignore les doublons si les clés sont identiques.

---

### 🟧 C) Restaurer une table inexistante
1. Créer la table dans **Table Editor → Create Table**.
2. Importer le CSV.

➡️ La structure doit correspondre aux colonnes du CSV.

---

### 🟩 Notes importantes :
- Le restore **ne doit pas être automatisé dans Streamlit** (risque d’écraser des données).
- Toujours restaurer via **Supabase**, car c’est sécurisé.
- Faire un backup avant chaque mise à jour importante.
""")

