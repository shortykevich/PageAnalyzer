import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def init_connection():
    try:
        connection = psycopg2.connect(DATABASE_URL)
    except Exception as e:
        return e
    return connection


def commit_transaction(connection):
    connection.commit()
    return None


def close_connection(connection):
    connection.close()
    return None


def get_all_urls():
    with init_connection() as conn:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("""
        SELECT
            id,
            name
        FROM urls
        ORDER BY id DESC
        """)
        rows = cursor.fetchall()
    commit_transaction(conn)
    close_connection(conn)
    return rows


def get_url_by_name(name):
    with init_connection() as conn:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("""
        SELECT
            id,
            name,
            to_char(created_at, 'YYYY-MM-DD') AS created
        FROM urls
        WHERE name=%s
        """, (name,))
        row = cursor.fetchone()
    commit_transaction(conn)
    close_connection(conn)
    return row if row else None


def add_url(url):
    with init_connection() as conn:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("""
            INSERT INTO urls (name, created_at)
            VALUES (%s, NOW())
            RETURNING id
        """, (url,))
        row = cursor.fetchone()
    commit_transaction(conn)
    close_connection(conn)
    return row


def get_url_by_id(id):
    with init_connection() as conn:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("""
        SELECT
            name,
            to_char(created_at, 'YYYY-MM-DD') AS created
        FROM urls
        WHERE id=%s
        """, (id,))
        row = cursor.fetchone()
    commit_transaction(conn)
    close_connection(conn)
    return row if row else None
