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


def get_list_urls():
    with init_connection() as conn:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("""
            SELECT
                u.id,
                u.name,
                to_char(MAX(uc.created_at), 'YYYY-MM-DD') as last_check_at
            FROM urls AS u
            LEFT JOIN url_checks AS uc
                ON uc.url_id = u.id
            GROUP BY u.id, u.name
            ORDER BY u.id DESC, last_check_at DESC
        """)
        rows = cursor.fetchall()
    commit_transaction(conn)
    close_connection(conn)
    return rows


def add_url(url):
    with init_connection() as conn:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("""
            INSERT INTO urls (name) VALUES (%s) RETURNING id
        """, (url,))
        row = cursor.fetchone()
    commit_transaction(conn)
    close_connection(conn)
    return row


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


def get_url_checks(id):
    with init_connection() as conn:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("""
            SELECT
                id,
                url_id,
                status_code,
                h1,
                title,
                description,
                to_char(created_at, 'YYYY-MM-DD') AS created
            FROM url_checks
            WHERE url_id = %s
            ORDER BY id DESC
        """, (id,))
        rows = cursor.fetchall()
    commit_transaction(conn)
    close_connection(conn)
    return rows


def add_url_check(id):
    with init_connection() as conn:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("""
            INSERT INTO url_checks (url_id) VALUES (%s) RETURNING id
        """, (id,))
        row = cursor.fetchone()
    commit_transaction(conn)
    close_connection(conn)
    return row
