import mysql.connector
from mysql.connector import Error
from db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST, user=DB_USER,
            password=DB_PASSWORD, database=DB_NAME
        )
    except Error as e:
        print(f"[DB ERROR] {e}")
        return None


if __name__ == "__main__":
    c = get_connection()
    print("OK" if c else "FAILED")
    if c:
        c.close()