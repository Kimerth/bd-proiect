import cx_Oracle
from configparser import ConfigParser

def connect():
    config = ConfigParser()
    config.read("db.config")

    db_cfg = config['oracle.sql']
    pool = cx_Oracle.SessionPool(db_cfg['usr'], db_cfg['pwrd'], db_cfg['conn'],
                             min = 2, max = 5, increment = 1, threaded = True)
    return pool

def cursor(pool):
    return pool.acquire().cursor()

def get_users(pool):
    csr = cursor(pool)
    csr.execute('SELECT * FROM "Researchers"')
    return csr

def get_tools(pool):
    csr = cursor(pool)
    csr.execute('SELECT * FROM "Tools"')
    return csr

def get_experiments(pool):
    csr = cursor(pool)
    csr.execute('SELECT * FROM "Experiments"')
    return csr

def get_results(pool):
    csr = cursor(pool)
    csr.execute('SELECT * FROM "Results"')
    return csr

def get_departments(pool):
    csr = cursor(pool)
    csr.execute('SELECT * FROM "Departments"')
    return csr

def get_buildings(pool):
    csr = cursor(pool)
    csr.execute('SELECT * FROM "Buildings"')
    return csr

pool = connect()
print("Database version:", pool.acquire().version)