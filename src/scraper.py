import os
import asyncio
import sys
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession # Добавили импорт
from supabase import create_client
from src.db import get_active_channels, update_last_message_id

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session_string = os.getenv('SESSION_STRING') # Добавили переменную
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

if not api_id or not api_hash or not session_string:
    raise ValueError("ОДНА ИЛИ НЕСКОЛЬКО ПЕРЕМЕННЫХ ОКРУЖЕНИЯ НЕ ЗАГРУЖЕНЫ!")
else:
    api_id = int(api_id)

async def run_scraper():
    channels = get_active_channels()
    if not channels:
        print('Нет активных каналов для обработки.')
        return

    # Инициализация клиента через StringSession
    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
        for username in channels:
            try:
                print(f'--- Обработка канала: {username} ---')
                await asyncio.sleep(2)
                
                messages = await client.get_messages(username, limit=50)

                max_id = 0
                for message in messages:
                    if not message.text:
                        continue
                    
                    if message.id > max_id:
                        max_id = message.id
                        
                    vacancy_data = {
                        "title": (message.text[:47] + '...') if len(message.text) > 50 else message.text,
                        "url": f"https://t.me/{username}/{message.id}",
                        "description": message.text,
                        "status": "new"
                    }
                    
                    try:
                        supabase.table("vacancies").insert(vacancy_data).execute()
                        print(f"Вакансия добавлена: {vacancy_data['url']}")
                    except Exception:
                        pass 

                if max_id > 0:
                    update_last_message_id(username, max_id)
                    print(f"Обновлен last_message_id для {username}: {max_id}")

            except Exception as e:
                print(f'Ошибка при работе с каналом {username}: {e}')
                await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(run_scraper())