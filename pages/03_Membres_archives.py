import streamlit as st
from menu import hide_streamlit_menu, menu_lateral
from supabase import create_client
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Membres archivés", page_icon="📁")
hide_streamlit_menu()
menu_lateral()

st.title("📁 Membres archivés")

# --- SUPABASE ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# --- LOAD DATA ---
response = supabase.table("membres").select("*").eq("archive", True).execute()
membres_archives = pd.DataFrame(response.data)

if membres_archives.empty:
    st.info("Aucun membre archivé.")
else:
    st.dataframe(
        membres_archives[
            ["id", "nom", "prenom", "email", "telephone", "date_archivage"]
        ],
        use_container_width=True
    )
