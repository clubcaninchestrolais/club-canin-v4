import streamlit as st
from supabase import create_client, Client
import datetime

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

aujourdhui = datetime.date.today().isoformat()

seances = (
    supabase.table("cours_seances")
    .select("*")
    .eq("date_seance", aujourdhui)
    .execute()
    .data
)

st.write("Cours_id réels et types :")
for s in seances:
    st.write(s["cours_id"], type(s["cours_id"]))
