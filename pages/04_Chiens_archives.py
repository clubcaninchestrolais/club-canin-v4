import streamlit as st
from menu import hide_streamlit_menu, menu_lateral
from supabase import create_client
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Chiens archivés", page_icon="📁")
hide_streamlit_menu()
menu_lateral()

st.title("📁 Chiens archivés")

# --- SUPABASE ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# --- LOAD DATA ---
response = supabase.table("chiens").select("*").eq("archive", True).execute()
chiens_archives = pd.DataFrame(response.data)

if chiens_archives.empty:
    st.info("Aucun chien archivé.")
else:
    st.dataframe(
        chiens_archives[
            ["id", "nom_chien", "race", "date_naissance", "id_membre", "date_archivage"]
        ],
        use_container_width=True
    )
