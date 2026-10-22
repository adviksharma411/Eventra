# db.py - Central place for database connection
# Every other file will import from here, so we write it ONCE.

import mysql.connector
from db_config import host, user, password, database


def get_connection():
    """Returns a fresh MySQL connection to the Eventra database."""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Database connection failed: {e}")
        return None