from telethon.sessions import StringSession
from telethon.sync import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

# Убедитесь, что здесь точно имя вашего файла сессии (без расширения)
session_name = 'new_worker_session'

# Мы создаем объект клиента, используя существующий файл
client = TelegramClient(session_name, os.getenv('API_ID'), os.getenv('API_HASH'))

# Используем метод, который просто загружает данные из файла в StringSession
# без попытки подключения к серверам Telegram
string_session = StringSession.save(client.session)

print("\n--- СКОПИРУЙТЕ ЭТУ СТРОКУ ДЛЯ RENDER ---")
print(string_session)
print("-------------------------------------------\n")