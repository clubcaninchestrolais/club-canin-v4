import streamlit as st
from supabase import create_client, Client

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------

SUPABASE_URL = "https://gdokaxnghwilduhqqgow.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdkb2theG5naHdpbGR1aHFxZ293Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjMwNjM5MCwiZXhwIjoyMDk3ODgyMzkwfQ.xb-oG4XWibesc0HZnBd3Pq1ORZNVvdWnwTOeqwwe5D0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------------------------------------
# AUDIT LOG
# ---------------------------------------------------------

def log_action(action: str, details: str = ""):
    """Ajoute une ligne dans le journal des actions."""
    try:
        supabase.table("audit_log").insert({
            "user_id": st.session_state.get("user_id", "inconnu"),
            "action": action,
            "details": details
        }).execute()
    except Exception as e:
        st.error(f"Erreur audit log : {e}")

# ---------------------------------------------------------
# MEMBRES
# ---------------------------------------------------------

def get_members():
    return supabase.table("membres") \
        .select("*") \
        .order("nom") \
        .execute().data

def get_member_by_id(membre_id):
    return (
        supabase
        .table("membres")
        .select("*")
        .eq("id", membre_id)
        .single()
        .execute()
        .data
    )

def add_member(data):
    result = supabase.table("membres").insert(data).execute()
    log_action("Ajout membre", f"{data.get('prenom', '')} {data.get('nom', '')}")
    return result

# ---------------------------------------------------------
# CHIENS
# ---------------------------------------------------------

def get_dogs():
    return supabase.table("chiens") \
        .select("*") \
        .order("nom") \
        .execute().data

def get_dog_by_id(dog_id):
    return supabase.table("chiens") \
        .select("*") \
        .eq("id", dog_id) \
        .execute().data[0]

def add_dog(data):
    result = supabase.table("chiens").insert(data).execute()
    log_action("Ajout chien", f"{data.get('nom', '')} (membre {data.get('id_membre', '')})")
    return result

# ---------------------------------------------------------
# COURS — PRÉSENCES DES CHIENS
# ---------------------------------------------------------

def get_cours_presences_for_dog(dog_id):
    return supabase.table("cours_presences") \
        .select("*") \
        .eq("id_chien", dog_id) \
        .order("date", desc=True) \
        .execute().data

# ---------------------------------------------------------
# COTISATIONS
# ---------------------------------------------------------

def get_cotisations():
    return supabase.table("cotisations") \
        .select("*") \
        .order("date_paiement", desc=True) \
        .execute().data

def get_cotisations_for_member(membre_id):
    return supabase.table("cotisations") \
        .select("*") \
        .eq("id_membres", membre_id) \
        .order("date_paiement", desc=True) \
        .execute().data

def add_cotisation(data):
    result = supabase.table("cotisations").insert({
        "id_membres": data["id_membres"],
        "montant": data["montant"],
        "date_paiement": data["date_paiement"],
        "date_expiration": data["date_expiration"],
        "statut": data["statut"],
        "remarques": data["remarques"],
    }).execute()

    log_action("Ajout cotisation", f"Membre {data['id_membres']} montant {data['montant']}")

    return result
