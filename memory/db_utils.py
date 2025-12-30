import json
import sqlite3
import os

class DBUtils:
    def __init__(self, db_path="career_data.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                profile_data TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                requirements TEXT,
                location TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_user_profile(self, username, profile_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (username, profile_data)
            VALUES (?, ?)
        ''', (username, json.dumps(profile_data)))
        conn.commit()
        conn.close()

    def get_user_profile(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT profile_data FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        return json.loads(row[0]) if row else None
