import sqlite3

DB_NAME = "room_details.db"

def get_connection():
    """Returns a new database connection."""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Initializes the database with required tables."""
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS room (
                room_no INTEGER PRIMARY KEY,
                col INTEGER,
                row INTEGER,
                seat INTEGER
            )
        """)
    conn.close()

def execute_query(query, params=()):
    """Executes a query and commits changes."""
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

def fetch_query(query, params=(), fetchone=False):
    """Fetches data from the database."""
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone() if fetchone else cursor.fetchall()
