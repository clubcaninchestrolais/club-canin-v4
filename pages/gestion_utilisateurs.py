import streamlit as st
import hashlib
from supabase_rest import supabase

# --- Sécurité ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

# --- Accès réservé à l'admin ---
if st.session_state.get("role") != "admin":
    st.error("Accès réservé à l'administrateur.")
    st.stop()

st.set_page_config(page_title="Gestion des utilisateurs", page_icon="🔐")
st.title("🔐 Gestion des utilisateurs")

# --- Fonction hash ---
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

# --- Charger les utilisateurs ---
users = supabase.table("utilisateurs").select("*").execute().data

st.subheader("👥 Utilisateurs existants")

for u in users:
    st.markdown(f"### {u['username']}")
    st.write(f"Rôle : **{u['role']}**")
    st.write(f"Actif : {'🟢 Oui' if u['actif'] else '🔴 Non'}")

    # Activer / désactiver
    if st.button(f"Activer / Désactiver {u['username']}", key=f"toggle_{u['id']}"):
        supabase.table("utilisateurs").update({"actif": not u["actif"]}).eq("id", u["id"]).execute()
        st.rerun()

    # Modifier mot de passe
    new_pwd = st.text_input(f"Nouveau mot de passe pour {u['username']}", type="password", key=f"pwd_{u['id']}")
    if st.button(f"Modifier mot de passe de {u['username']}", key=f"pwd_btn_{u['id']}"):
        hashed = hash_password(new_pwd)
        supabase.table("utilisateurs").update({"password_hash": hashed}).eq("id", u["id"]).execute()
        st.success("Mot de passe mis à jour.")
        st.rerun()

    st.markdown("---")

# --- Ajouter un utilisateur ---
st.subheader("➕ Ajouter un utilisateur")

new_user = st.text_input("Nom d'utilisateur")
new_pwd = st.text_input("Mot de passe", type="password")
new_role = st.selectbox("Rôle", ["admin", "user"])

if st.button("Créer l'utilisateur"):
    hashed = hash_password(new_pwd)
    supabase.table("utilisateurs").insert({
        "username": new_user,
        "password_hash": hashed,
        "role": new_role,
        "actif": True
    }).execute()
    st.success("Utilisateur créé.")
    st.rerun()
