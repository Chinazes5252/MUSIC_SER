import sqlite3
from datetime import datetime
import hashlib

class Database:
    def __init__(self, db_name: str = 'music_bot.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                last_access DATETIME
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                artist TEXT,
                duration INTEGER,
                file_hash TEXT UNIQUE,
                file_path TEXT,
                timestamp DATETIME,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        self.conn.commit()

    def add_track(self, user_id: int, title: str, artist: str, duration: int, file_path: str) -> bool:
        file_hash = hashlib.md5(open(file_path,'rb').read()).hexdigest()
        cur = self.conn.cursor()
        cur.execute('INSERT OR REPLACE INTO users (user_id, last_access) VALUES (?, ?)',
                    (user_id, datetime.now()))
        try:
            cur.execute(
                'INSERT INTO tracks (user_id, title, artist, duration, file_hash, file_path, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (user_id, title, artist, duration, file_hash, file_path, datetime.now())
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user_tracks(self, user_id: int, limit: int = 10):
        cur = self.conn.cursor()
        cur.execute(
            'SELECT title, artist, duration, file_path FROM tracks WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
            (user_id, limit)
        )
        return cur.fetchall()

    def close(self):
        self.conn.close()