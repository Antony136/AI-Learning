import psycopg

from app.core.config import DATABASE_URL


def get_connection():
    return psycopg.connect(DATABASE_URL)