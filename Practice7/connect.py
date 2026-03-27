import psycopg2
from config import load_config

def connect():
    try:
        config = load_config()

        conn = psycopg2.connect(**config)
        print("Connected to the PostgreSQL server successfully!")

        conn.close()

    except (psycopg2.DatabaseError, Exception) as error:
        print("Error:", error)

if __name__ == '__main__':
    connect()