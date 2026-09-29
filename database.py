import sqlite3
from pathlib import Path

DB = Path("viralbot.db")

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def setup():
    conn = connect()
    conn.execute("""CREATE TABLE IF NOT EXISTS jobs(
        id TEXT PRIMARY KEY, status TEXT, progress INTEGER DEFAULT 0,
        topic TEXT, created TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS uploads(
        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT,
        youtube_id TEXT, created TEXT)""")
    conn.commit()
    conn.close()

setup()
