import streamlit as st
from supabase import create_client, Client

# ---------------------------------------------------------
# Connexion Supabase
# ---------------------------------------------------------

SUPABASE_URL = "https://gdokaxnghwilduhqqgow.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdkb2theG5naHdpbGR1aHFxZ293Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjMwNjM5MCwiZXhwIjoyMDk3ODgyMzkwfQ.xb-oG4XWibesc0HZnBd3Pq1ORZNVvdWnwTOeqwwe5D0"

supabase_raw: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------------------------------------
# AUDIT LOG
# ---------------------------------------------------------

def log_action(action: str, details: str = ""):
    """Ajoute une ligne dans le journal des actions."""
    try:
        supabase_raw.table("audit_log").insert({
            "user_id": st.session_state.get("user_id", "inconnu"),
            "action": action,
            "details": details
        }).execute()
    except Exception as e:
        st.error(f"Erreur audit log : {e}")

# ---------------------------------------------------------
# WRAPPER AUTOMATIQUE POUR LES INSERTIONS MEMBRES
# ---------------------------------------------------------

class SupabaseWrapper:
    def __init__(self, client):
        self.client = client

    def table(self, table_name):
        original_table = self.client.table(table_name)

        # Si ce n'est pas la table membres → comportement normal
        if table_name != "membres":
            return original_table

        # Sinon on crée un wrapper spécial
        class TableWrapper:
            def __init__(self, table):
                self.table = table

            def insert(self, data):
                # Insertion normale
                result = self.table.insert(data).execute()

                # Si insertion OK → log automatique
                if result.data:
                    try:
                        prenom = data.get("prenom", "")
                        nom = data.get("nom", "")
                        log_action("Ajout membre", f"{prenom} {nom}")
                    except Exception as e:
                        st.error(f"Erreur audit log : {e}")

                return result

            # Toutes les autres méthodes restent accessibles
            def __getattr__(self, name):
                return getattr(self.table, name)

        return TableWrapper(original_table)


# On remplace supabase par notre wrapper
supabase = SupabaseWrapper(supabase_raw)

# ---------------------------------------------------------
# MEMBRES (lecture)
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
    result = supabase_raw.table("chiens").insert(data).execute()
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
    result = supabase_raw.table("cotisations").insert({
        "id_membres": data["id_membres"],
        "montant": data["montant"],
        "date_paiement": data["date_paiement"],
        "date_expiration": data["date_expiration"],
        "statut": data["statut"],
        "remarques": data["remarques"],
    }).execute()

    log_action("Ajout cotisation", f"Membre {data['id_membres']} montant {data['montant']}")

    return result
