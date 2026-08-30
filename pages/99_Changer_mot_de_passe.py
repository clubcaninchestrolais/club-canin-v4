import streamlit as st
from securite import securite_user
securite_user()

from datetime import datetime
from supabase_rest import supabase
import hashlib

st.title("Changer mon mot de passe")

# ---------------------------------------------------------
# Fonction de hash
# ---------------------------------------------------------
def hash_password(pwd: str):
    return hashlib.sha256(pwd.encode()).hexdigest()

# ---------------------------------------------------------
# Récupération de l'utilisateur connecté
# ---------------------------------------------------------
user_email = st.session_state.get("email")

if not user_email:
    st.error("Erreur : utilisateur non identifié.")
    st.stop()

# ---------------------------------------------------------
# Formulaire
# ---------------------------------------------------------
st.write("Cette fonction n'est pas encore activée par le club.")

old_pwd = st.text_input("Ancien mot de passe", type="password")
new_pwd = st.text_input("Nouveau mot de passe", type="password")
confirm_pwd = st.text_input("Confirmer le nouveau mot de passe", type="password")

if st.button("Changer le mot de passe"):
    st.warning("Cette fonction est désactivée pour le moment.")
