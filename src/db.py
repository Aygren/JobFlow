import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

def get_active_channels():
    """Получает список всех активных каналов с их последним обработанным ID."""
    response = supabase.table("active_channels")\
        .select("username, last_message_id")\
        .eq("is_active", True)\
        .execute()
    return response.data

def update_last_message_id(username, last_id):
    """Обновляет ID последнего сообщения для канала."""
    supabase.table("active_channels")\
        .update({"last_message_id": last_id})\
        .eq("username", username)\
        .execute()