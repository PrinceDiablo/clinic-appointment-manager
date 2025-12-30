import pymysql
from pymysql.cursors import DictCursor
from flask import current_app, g
from contextlib import contextmanager

def db_connect():
    """ 
    Establish a PyMySQL connection with MySQL db.
    """
    try:
        connection = pymysql.connect(
            host = current_app.config["MYSQL_HOST"],
            port = current_app.config["MYSQL_PORT"],
            user = current_app.config["MYSQL_USER"],
            password = current_app.config["MYSQL_PASSWORD"],
            database = current_app.config["MYSQL_DATABASE"],
            charset = 'utf8mb4',
            cursorclass = DictCursor
        )
        return connection
    except pymysql.Error as e:
        raise Exception(e)
    
def get_db():
    """ 
    Return a per-request PyMySQL connection stored on `flask.g`.
    """
    if "db" not in g:
        g.db = db_connect()
    return g.db

def close_db(e=None):
    """
    Close the db connection for the request if it exists.
    """
    db = g.pop("db", None)
    if db is not None:
        try:
            db.close()
        except Exception:
            pass

def fetchone(query, parameters=None) -> dict:
    """
    Helper function to execute a SELECT query and return a single row dict.

    Usage:
        row = fetchone("SELECT * FROM users WHERE id=%s",(id,))
    """
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query, parameters or ())
        return cursor.fetchone()

def fetchall(query, parameters=None) -> list[dict]:
    """
    Helper function to execute a SELECT query and return all rows as a list of dicts.

    Usage:
        rows = fetchall("SELECT * FROM appointments WHERE doctor_id=%s", (doctor_id,))
    """
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query, parameters or ())
        return cursor.fetchall()

def execute_commit(query, parameters=None) -> tuple[int, int]:
    """
    WARNING: Do NOT use inside a `transaction()` block. This function commits immediately.
    
    Helper function to execute INSERT/UPDATE/DELETE and commit. Returns rowcount and lastrowid.
    
    Usage:
        n = execute_commit("UPDATE users SET failed_logins = failed_logins+1 WHERE id=%s", (id,))
    """
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query, parameters or ())
    connection.commit()
    return cursor.rowcount, cursor.lastrowid

def execute(query, parameters=None) -> tuple[int, int]:
    """
    Helper function to execute INSERT/UPDATE/DELETE without committing. Returns rowcount and lastrowid.

    Usage:
        n = execute("UPDATE users SET failed_logins = failed_logins+1 WHERE id=%s", (id,))
    """
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query, parameters or ())
    return cursor.rowcount, cursor.lastrowid

@contextmanager
def transaction():
    """
    Ensures that all operations executed within the block are committed
    as a single transaction, or fully rolled back if an exception occurs.

    Usage:
        with transaction():
            execute("INSERT INTO users (...) VALUES (...)")
            execute("INSERT INTO user_roles (...) VALUES (...)")
    
    Instructions:
    - Use `execute()` for write operations inside this block.
    - Do NOT use `execute_commit()` inside a transaction.
    - Any exception inside the block triggers a rollback.        
    """
    db = get_db()
    try:
        db.begin()
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise