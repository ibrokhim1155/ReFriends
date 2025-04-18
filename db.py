import sqlite3


conn = sqlite3.connect("db_data/referral_bot.db")
cursor = conn.cursor()

def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            invited_by INTEGER,
            balance INTEGER DEFAULT 0,
            full_name TEXT,
            card_number TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            approved INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE
        )
    ''')

    conn.commit()
