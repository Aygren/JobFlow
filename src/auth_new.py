import os
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Удаляем/создаем новый клиент
client = TelegramClient('jobflow_session', api_id, api_hash)

async def main():
    # Вызываем start, но явно указываем phone, если нужно
    # Если скрипт зависнет после этой строки, значит проблема в сети
    print("Инициализация клиента...")
    await client.start()
    
    print("Подключение успешно!")
    me = await client.get_me()
    print(f"Вы вошли как: {me.username}")

with client:
    client.loop.run_until_complete(main())