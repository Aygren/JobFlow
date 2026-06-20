import sqlite3
import os

# Путь к базе данных внутри папки data/
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'vacancies.db')


def init_db():
    """Создает базу данных и таблицы, если они еще не существуют."""
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    last_message_id INTEGER,
                    is_active INTEGER NOT NULL DEFAULT 1
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vacancies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT,
                    url TEXT,
                    status TEXT NOT NULL DEFAULT 'new',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(channel_id) REFERENCES channels(id)
                )
            ''')

            conn.commit()

        return True
    except sqlite3.Error as exc:
        print(f"Ошибка инициализации БД: {exc}")
        return False


def add_channel(username):
    """Добавляет канал в таблицу channels, игнорируя дубли."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO channels (username)
                VALUES (?)
                ON CONFLICT(username) DO NOTHING
                ''',
                (username,)
            )
            conn.commit()
        return True
    except sqlite3.Error as exc:
        print(f"Ошибка при добавлении канала '{username}': {exc}")
        return False


def get_active_channels():
    """Возвращает список активных имен каналов."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT username
                FROM channels
                WHERE is_active = 1
            ''')
            rows = cursor.fetchall()
            return [row[0] for row in rows]
    except sqlite3.Error as exc:
        print(f"Ошибка при получении активных каналов: {exc}")
        return []


def update_last_message_id(username, message_id):
    """Обновляет поле last_message_id для указанного канала."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                UPDATE channels
                SET last_message_id = ?
                WHERE username = ?
                ''',
                (message_id, username)
            )
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as exc:
        print(f"Ошибка при обновлении last_message_id для {username}: {exc}")
        return False


__all__ = [
    'init_db',
    'add_channel',
    'get_active_channels',
    'update_last_message_id',
]


if __name__ == "__main__":
    init_db()
