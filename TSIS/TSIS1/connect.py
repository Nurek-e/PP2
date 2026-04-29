from psycopg2 import connect
from config import host, database, user, password


def get_connection():
    return connect(
        host=host,
        database=database,
        user=user,
        password=password,
        options="-c client_encoding=UTF8"
    )