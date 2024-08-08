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


def execute_sql(sql, params=(), fetchall=False):
    conn = init_connection()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(sql, params)
        result = cur.fetchall() if fetchall else cur.fetchone()
        commit_transaction(conn)
    close_connection(conn)
    return result


def get_urls_list():
    sql = """
        SELECT
            u.id,
            u.name,
            to_char(MAX(uc.created_at), 'YYYY-MM-DD') as last_check_at,
            uc.status_code
        FROM urls AS u
        LEFT JOIN url_checks AS uc
            ON uc.url_id = u.id
        GROUP BY u.id, u.name, uc.status_code
        ORDER BY u.id DESC, last_check_at DESC
    """
    return execute_sql(sql, fetchall=True)


def add_url(url):
    sql = """
        INSERT INTO urls (name) VALUES (%s) RETURNING id
    """
    return execute_sql(sql, (url,))


def get_url_by_name(name):
    sql = """
        SELECT
            id,
            name,
            to_char(created_at, 'YYYY-MM-DD') AS created
        FROM urls
        WHERE name=%s
    """
    return execute_sql(sql, params=(name,))


def get_url_by_id(id):
    sql = """
        SELECT
            name,
            to_char(created_at, 'YYYY-MM-DD') AS created
        FROM urls
        WHERE id=%s
    """
    return execute_sql(sql, params=(id,))


def get_url_checks(id):
    sql = """
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
    """
    return execute_sql(sql, params=(id,), fetchall=True)


def add_url_check(check):
    sql = """
        INSERT INTO url_checks (url_id, status_code, h1, title, description)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
    """
    return execute_sql(sql, params=tuple(check.values(),))
