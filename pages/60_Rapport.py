import streamlit as st
from securite import securite_admin
securite_admin()

from supabase_rest import supabase
from menu import hide_streamlit_menu, menu_lateral


st.set_page_config(page_title="Rapport", page_icon="📊")

st.title("📊 Rapport")
st.write("Page rapport en construction.")
