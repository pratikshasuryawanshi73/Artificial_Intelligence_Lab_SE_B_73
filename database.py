import pymysql

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "smart_agri"

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def fetch_all(query, args=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, args)
            return cursor.fetchall()
    finally:
        conn.close()

def fetch_one(query, args=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, args)
            return cursor.fetchone()
    finally:
        conn.close()

def execute_query(query, args=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, args)
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()
