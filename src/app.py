from flask import Flask
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Добавляет текущую папку (src) в пути поиска

import scraper

app = Flask(__name__)

import asyncio

@app.route('/run')
def run_job():
    print("DEBUG: Функция run_job вызвана!")
    
    # Запускаем асинхронную функцию через asyncio.run в отдельном потоке
    def start_async_task():
        asyncio.run(scraper.run_scraper())

    threading.Thread(target=start_async_task).start()
    return "Парсер запущен!", 200

@app.route('/')
def health_check():
    return "Бот готов к работе", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)