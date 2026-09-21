import sqlite3


DATABASE = "study_assistant.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def get_all_notes():
    connection = get_connection()

    notes = connection.execute("""
        SELECT * FROM notes
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return notes


def add_note(title, content):
    connection = get_connection()

    connection.execute("""
        INSERT INTO notes (title, content)
        VALUES (?, ?)
    """, (title, content))

    connection.commit()
    connection.close()


def delete_note(note_id):
    connection = get_connection()

    connection.execute("""
        DELETE FROM notes
        WHERE id = ?
    """, (note_id,))

    connection.commit()
    connection.close()