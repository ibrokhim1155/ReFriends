from db import cursor, conn

def register_user_if_needed(user_id: int, invited_by: int | None):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        return
    cursor.execute("INSERT INTO users (user_id, invited_by) VALUES (?, ?)", (user_id, invited_by))
    if invited_by and invited_by != user_id:
        cursor.execute("UPDATE users SET balance = balance + 500 WHERE user_id = ?", (invited_by,))
    conn.commit()