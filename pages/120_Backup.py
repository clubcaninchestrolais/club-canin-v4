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
    "presences",
    "cours_dates",
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

        except Exception as e:
            st.error(f"❌ Erreur lors de la lecture de la table : {table}")

# Bouton de téléchargement
st.download_button(
    label="📦 Télécharger le backup complet (ZIP)",
    data=zip_buffer.getvalue(),
    file_name="backup_club_canin.zip",
    mime="application/zip"
)
