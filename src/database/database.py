import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

def get_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        return None
    return create_client(url, key)

def save_transaction(supabase, desc, valor, tipo):
    data = {"description": desc, "amount": valor, "type": tipo}
    return supabase.table("transactions").insert(data).execute()

def fetch_transactions(supabase):
    return supabase.table("transactions").select("*").execute()