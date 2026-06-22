from flask import Flask
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Добавляет текущую папку (src) в пути поиска

import logging
# Настройка логгера для вывода в поток stdout (который видит Render)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

import scraper

app = Flask(__name__)

import asyncio

@app.route('/run')
def run_job():
    logger.info("DEBUG: Функция run_job вызвана!")
    
    def start_async_task():
        try:
            logger.info("DEBUG: Поток запущен.")
            asyncio.run(scraper.run_scraper())
            logger.info("DEBUG: Поток успешно завершен.")
        except Exception as e:
            logger.error(f"DEBUG: Ошибка в потоке: {e}")

    threading.Thread(target=start_async_task).start()
    return "Парсер запущен!", 200

@app.route('/')
def health_check():
    return "Бот готов к работе", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)