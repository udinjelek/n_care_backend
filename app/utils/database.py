import sqlite3
import mysql.connector
from app.config import DATABASE_CONFIG

# # sqlite3 connection
def get_db_connection():
    conn = sqlite3.connect('db/xn_care.db')
    conn.row_factory = sqlite3.Row  # Set row_factory to sqlite3.Row
    return conn

# # mysql connection
def mysql_get_db_connection():
    conn = mysql.connector.connect (
        host=DATABASE_CONFIG['host'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        database=DATABASE_CONFIG['database'],
        port=DATABASE_CONFIG['port']
    )
    print (DATABASE_CONFIG['host'],
           DATABASE_CONFIG['user'],
           DATABASE_CONFIG['password'],
           DATABASE_CONFIG['database'],
           DATABASE_CONFIG['port'])
    return conn

