from flask import Flask
import threading
import sys
import os
import logging
import asyncio

# Добавляем текущую папку в пути поиска
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настройка логгера для вывода в поток stdout
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

import scraper

app = Flask(__name__)

@app.route('/run')
def run_job():
    # ПРИНУДИТЕЛЬНЫЙ ВЫВОД ДЛЯ ОТЛАДКИ
    print("DEBUG_CHECK: Запрос /run получен сервером!", flush=True)
    logger.info("DEBUG: Функция run_job вызвана!")
    
    def start_async_task():
        try:
            print("DEBUG_CHECK: Запуск scraper.run_scraper...", flush=True)
            logger.info("DEBUG: Поток запущен.")
            asyncio.run(scraper.run_scraper())
            print("DEBUG_CHECK: Скрипт завершился успешно.", flush=True)
            logger.info("DEBUG: Поток успешно завершен.")
        except Exception as e:
            print(f"DEBUG_CHECK: КРИТИЧЕСКАЯ ОШИБКА В ПОТОКЕ: {e}", flush=True)
            logger.error(f"DEBUG: Ошибка в потоке: {e}")

    threading.Thread(target=start_async_task).start()
    return "Парсер запущен!", 200

@app.route('/')
def health_check():
    return "Бот готов к работе", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)