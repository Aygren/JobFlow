import os
import asyncio

from dotenv import load_dotenv
from telethon import TelegramClient, errors
from src.db import get_active_channels, update_last_message_id


async def run_scraper():
    load_dotenv()

    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')

    if not api_id or not api_hash:
        print('API_ID и API_HASH должны быть заданы в переменных окружения.')
        return

    try:
        api_id = int(api_id)
    except ValueError:
        print('API_ID должен быть числом.')
        return

    channels = get_active_channels()
    if not channels:
        print('Нет активных каналов для обработки.')
        return

    try:
        async with TelegramClient('jobflow_session', api_id, api_hash) as client:
            for username in channels:
                last_message_id = 0
                try:
                    messages = await client.get_messages(username, min_id=last_message_id, limit=100)

                    if not messages:
                        print(f'Канал {username}: новых сообщений нет.')
                        continue

                    max_id = 0
                    for message in messages:
                        message_text = message.text if hasattr(message, 'text') else getattr(message, 'message', None)
                        print(f'Канал={username} message_id={message.id} text={message_text}')
                        if message.id and message.id > max_id:
                            max_id = message.id

                    if max_id > 0:
                        update_last_message_id(username, max_id)
                except (errors.RPCError, ConnectionError, OSError) as exc:
                    print(f'Ошибка при получении сообщений для канала {username}: {exc}')
    except errors.RPCError as exc:
        print(f'Ошибка авторизации или Telegram RPC: {exc}')
    except (ConnectionError, OSError) as exc:
        print(f'Ошибка сети при подключении к Telegram: {exc}')


if __name__ == '__main__':
    asyncio.run(run_scraper())
