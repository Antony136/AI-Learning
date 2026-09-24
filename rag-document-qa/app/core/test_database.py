import os

import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")

if not DATABASE_URL_TEST:
    raise ValueError(
        "DATABASE_URL_TEST is not set in the .env file"
    )


def get_test_connection():
    return psycopg.connect(DATABASE_URL_TEST)

from app.core.database import get_connection

