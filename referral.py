from db import cursor, conn

def add_user(user_id: int, invited_by: int | None):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        return
    cursor.execute("INSERT INTO users (user_id, invited_by) VALUES (?, ?)", (user_id, invited_by))
    if invited_by:
        cursor.execute("UPDATE users SET balance = balance + 500 WHERE user_id = ?", (invited_by,))
    conn.commit()

def get_balance(user_id):
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()[0]
