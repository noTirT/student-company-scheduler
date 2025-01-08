import sqlite3

from src.util.functions import get_db_location


def get_db_connection():
    database_url = get_db_location()
    conn = sqlite3.connect(database_url)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    script = """
    CREATE TABLE IF NOT EXISTS company (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        block1_slots TEXT NOT NULL,
        block2_slots TEXT NOT NULL,
        capacity INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS student_selection (
        student_id INTEGER,
        company_id INTEGER,
        block INTEGER,
        slot INTEGER,
        PRIMARY KEY (student_id, company_id, block, slot),
        FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE,
        FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
    );

    PRAGMA foreign_keys = ON;
    """
    cursor.executescript(script)

    conn.commit()
    conn.close()
