import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "healthcare.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                medicine TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                note TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_message TEXT NOT NULL,
                bot_reply TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )"""
        )

def create_user(username, password_hash):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password_hash),
        )
        return conn.execute(
            "SELECT id FROM users WHERE username=?",
            (username,),
        ).fetchone()["id"]

def get_user(username):
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,),
        ).fetchone()

def add_reminder(user_id, medicine, reminder_time, note=""):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO reminders (user_id, medicine, reminder_time, note) VALUES (?, ?, ?, ?)",
            (user_id, medicine, reminder_time, note),
        )

def list_reminders(user_id):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM reminders WHERE user_id=? ORDER BY reminder_time DESC",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]

def log_conversation(user_id, user_message, bot_reply):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO conversations (user_id, user_message, bot_reply) VALUES (?, ?, ?)",
            (user_id, user_message, bot_reply),
        )
