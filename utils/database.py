import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "database", "phishing.db")


def create_tables():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    # History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        scan_type TEXT,
        input_text TEXT,
        prediction TEXT,
        scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# Add New User
def add_user(name, email, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()
def check_user(email):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    conn.close()
    return user
def save_history(user_email, scan_type, input_text, prediction):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history(user_email, scan_type, input_text, prediction)
        VALUES (?, ?, ?, ?)
    """, (user_email, scan_type, input_text, prediction))

    conn.commit()
    conn.close()


def get_history(user_email):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT scan_type, input_text, prediction, scan_time
        FROM history
        WHERE user_email = ?
        ORDER BY scan_time DESC
    """, (user_email,))

    history = cursor.fetchall()

    conn.close()

    return history
def get_statistics(user_email):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM history WHERE user_email=? AND scan_type='SMS'",
        (user_email,)
    )
    sms = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM history WHERE user_email=? AND scan_type='Email'",
        (user_email,)
    )
    email = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM history WHERE user_email=? AND scan_type='URL'",
        (user_email,)
    )
    url = cursor.fetchone()[0]

    total = sms + email + url

    conn.close()

    return sms, email, url, total