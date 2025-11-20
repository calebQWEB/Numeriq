from fastapi import Depends, HTTPException
from supabase import create_client, Client
from app.config.settings import settings

async def get_supabase_client() -> Client:
    try:
        client = create_client(settings.supabase_url, settings.supabase_key)
        return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize Supabase client: {str(e)}")