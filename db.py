import mysql.connector
from mysql.connector import Error
from db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Error as e:
        print(f"[DB ERROR] Could not connect to MySQL: {e}")
        return None


if __name__ == "__main__":
    c = get_connection()
    if c:
        print("Database connection OK.")
        c.close()
    else:
        print("Database connection FAILED.")