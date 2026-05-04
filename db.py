import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def fetch_pending(cursor):
    cursor.execute("""
        SELECT * FROM recipients 
        WHERE status = 'Pending' OR (status = 'Failed' AND retry_count < 2)
    """)
    return cursor.fetchall()

def update_status(cursor, user_id, status, error=None):
    cursor.execute("""
        UPDATE recipients 
        SET status = %s,
            sent_at = NOW(),
            retry_count = retry_count + IF(%s='Failed',1,0),
            last_error = %s
        WHERE id = %s
    """, (status, status, error, user_id))