from supabase_rest import create_auth_user, upsert_profile


def create_user_with_profile(email: str, password: str, role: str):
    user_id = create_auth_user(email, password)
    upsert_profile(user_id, email, role)
    return user_id