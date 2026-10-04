import sqlite3


DATABASE = "study_assistant.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    # Users table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Notes table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()


def create_user(username, password):
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, password))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_user_by_username(username):
    connection = get_connection()

    user = connection.execute("""
        SELECT * FROM users
        WHERE username = ?
    """, (username,)).fetchone()

    connection.close()

    return user


def get_all_notes(user_id):
    connection = get_connection()

    notes = connection.execute("""
        SELECT * FROM notes
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,)).fetchall()

    connection.close()

    return notes


def add_note(title, content, user_id):
    connection = get_connection()

    connection.execute("""
        INSERT INTO notes (title, content, user_id)
        VALUES (?, ?, ?)
    """, (title, content, user_id))

    connection.commit()
    connection.close()


def delete_note(note_id, user_id):
    connection = get_connection()

    connection.execute("""
        DELETE FROM notes
        WHERE id = ? AND user_id = ?
    """, (note_id, user_id))

    connection.commit()
    connection.close()
    
