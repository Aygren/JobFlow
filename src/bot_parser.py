import os
from telethon import TelegramClient
from telethon.sessions import StringSession # Добавили импорт
from supabase import create_client
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Инициализация клиентов через StringSession
session_string = os.getenv('SESSION_STRING')
client = TelegramClient(StringSession(session_string), os.getenv('API_ID'), os.getenv('API_HASH'))
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

async def main():
    channel_username = 'sova_freelance'
    
    print(f"Читаем последние сообщения из {channel_username}...")
    
    async for message in client.iter_messages(channel_username, limit=5):
        if message.text:
            data = {
                "title": message.text[:50] + "...", 
                "url": f"https://t.me/{channel_username}/{message.id}",
                "description": message.text
            }
            try:
                supabase.table("vacancies").insert(data).execute()
                print(f"Добавлена вакансия: {data['url']}")
            except Exception as e:
                print(f"Ошибка при вставке в базу: {e}")

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())