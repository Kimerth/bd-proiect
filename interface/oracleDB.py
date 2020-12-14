import cx_Oracle
from configparser import ConfigParser

def connect():
    config = ConfigParser()
    config.read("db.config")

    db_cfg = config['oracle.sql']
    pool = cx_Oracle.SessionPool(db_cfg['usr'], db_cfg['pwrd'], db_cfg['conn'],
                             min = 2, max = 5, increment = 1, threaded = True)
    return pool

def cursor(conn):
    csr = conn.cursor()
    return csr

pool = connect()
conn = pool.acquire()
print("Database version:", conn.version)