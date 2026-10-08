import mysql.connector
from db_config import host, user, password, database

try:
    conn = mysql.connector.connect(
        host=host, user=user, password=password, database=database
    )
    if conn.is_connected():
        print("✅ Connected to Eventra database successfully!")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")