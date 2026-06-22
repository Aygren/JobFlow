from flask import Flask
import threading
from . import scraper

app = Flask(__name__)

@app.route('/run')
def run_job():
    # Запускаем парсер в отдельном потоке, чтобы не блокировать веб-сервер
    threading.Thread(target=scraper.run_scraper).start()
    return "Парсер запущен!", 200

@app.route('/')
def health_check():
    return "Бот готов к работе", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)