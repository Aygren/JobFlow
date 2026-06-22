import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from supabase import create_client
from db import get_active_channels, update_last_message_id

# Настройка переменных
raw_api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
session_string = os.environ.get('SESSION_STRING')
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

# Проверка переменных
if not all([raw_api_id, api_hash, session_string, supabase_url, supabase_key]):
    missing = [k for k, v in {"API_ID": raw_api_id, "API_HASH": api_hash, 
                              "SESSION_STRING": session_string, "SUPABASE_URL": supabase_url, 
                              "SUPABASE_KEY": supabase_key}.items() if not v]
    print(f"КРИТИЧЕСКАЯ ОШИБКА: Отсутствуют переменные окружения: {', '.join(missing)}")
    supabase = None
    api_id = 0
else:
    api_id = int(raw_api_id)
    supabase = create_client(supabase_url, supabase_key)

async def run_scraper():
    if not supabase or api_id == 0:
        print("Парсер не может запуститься: нет настроек.")
        return

    channels = get_active_channels()
    if not channels:
        print('Нет активных каналов для обработки.')
        return

    # Инициализация клиента с использованием сессии
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
    
    # КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: 
    # Вместо простого 'async with client:' вызываем start() с параметром,
    # который предотвращает запрос авторизации, если сессия уже есть.
    await client.start()
    
    print("Подключение к Telegram успешно...", flush=True)
    
    try:
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
                        print(f"Вакансия добавлена: {vacancy_data['url']}", flush=True)
                    except Exception as e:
                        print(f"Ошибка при вставке в Supabase: {e}")

                if max_id > 0:
                    update_last_message_id(username, max_id)
                    print(f"Обновлен last_message_id для {username}: {max_id}")

            except Exception as e:
                print(f'Ошибка при работе с каналом {username}: {e}')
                await asyncio.sleep(5)
    finally:
        # Корректное закрытие сессии
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(run_scraper())