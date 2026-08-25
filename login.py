import streamlit as st
from supabase_rest import supabase
import hashlib

st.set_page_config(page_title="Connexion", page_icon="🔐")

st.title("🔐 Connexion au Club Canin")

# ---------------------------------------------------------
# Fonction de hash
# ---------------------------------------------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------------------------------------------
# Si déjà connecté → redirection
# ---------------------------------------------------------
if st.session_state.get("connected", False):
    st.switch_page("pages/00_Accueil.py")

# ---------------------------------------------------------
# Formulaire de connexion
# ---------------------------------------------------------
username = st.text_input("Nom d'utilisateur")
password = st.text_input("Mot de passe", type="password")

if st.button("Connexion"):
    # Charger l'utilisateur
    user = (
        supabase.table("utilisateurs")
        .select("*")
        .eq("username", username)
        .execute()
        .data
    )

    if not user:
        st.error("Utilisateur inconnu.")
    else:
        user = user[0]

        if not user["actif"]:
            st.error("Ce compte est désactivé.")
        else:
            # Vérification du mot de passe
            if hash_password(password) == user["password_hash"]:
                # Stockage session
                st.session_state["connected"] = True
                st.session_state["username"] = user["username"]
                st.session_state["role"] = user["role"]
                st.session_state["uuid"] = user["uuid"]

                st.success("Connexion réussie.")
                st.switch_page("pages/00_Accueil.py")
            else:
                st.error("Mot de passe incorrect.")

# ---------------------------------------------------------
# Message d'aide
# ---------------------------------------------------------
st.markdown("---")
st.info("Veuillez entrer vos identifiants pour accéder à l'application.")
