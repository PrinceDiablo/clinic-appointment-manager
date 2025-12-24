import pymysql
from pymysql.cursors import DictCursor
from flask import current_app, g

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

def fetchone(query, parameters=None):
    """
    Helper function to execute: SELECT and return a single row dict.
    Usage:
        row = fetchone("SELECT * FROM users WHERE id=%s",(id,))
    """
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query, parameters or ())
        return cursor.fetchone()
    
def execute_commit(query, parameters=None) -> list:
    """
    Helper function to execute: INSERT/UPDATE/DELETE and commit. Returns rowcount and lastrowid
    Usage:
        n = execute_commit("UPDATE users SET failed_logins = failed_logins+1 WHERE id=%s", (id,))
    """
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query, parameters or ())
    connection.commit()
    return cursor.rowcount, cursor.lastrowid