from flask import Flask
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Добавляет текущую папку (src) в пути поиска

import scraper

app = Flask(__name__)

@app.route('/run')
def run_job():
    print("DEBUG: Функция run_job вызвана!")  # Это должно появиться в логах
    # Запускаем парсер в отдельном потоке, чтобы не блокировать веб-сервер
    threading.Thread(target=scraper.run_scraper).start()
    return "Парсер запущен!", 200

@app.route('/')
def health_check():
    return "Бот готов к работе", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)