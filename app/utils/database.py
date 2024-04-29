import sqlite3

def get_db_connection():
    conn = sqlite3.connect('db/xn_care.db')
    conn.row_factory = sqlite3.Row  # Set row_factory to sqlite3.Row
    return conn