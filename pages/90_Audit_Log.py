import streamlit as st
from securite import securite_admin
securite_admin()

from supabase_rest import supabase
import pandas as pd

st.set_page_config(page_title="📜 Journal des actions", page_icon="📜", layout="wide")

st.title("📜 Journal des actions")
st.write("Historique complet des actions effectuées dans l'application.")

st.markdown("---")

try:
    # Récupération des logs
    data = (
        supabase
        .table("audit_log")
        .select("*")
        .order("date", desc=True)
        .execute()
        .data
    )

    if not data:
        st.info("Aucune action enregistrée pour le moment.")
    else:
        df = pd.DataFrame(data)

        # Mise en forme des dates
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d/%m/%Y %H:%M:%S")

        # Affichage
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("Impossible de charger le journal des actions.")
    st.write(e)
