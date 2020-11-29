import cx_Oracle
from configparser import ConfigParser

if __name__ == "__main__":
    config = ConfigParser()
    config.read("db.config")

    db_cfg = config['oracle.sql']
    conn = cx_Oracle.connect(db_cfg['usr'], db_cfg['pwrd'], db_cfg['conn'])
    print("Database version:", conn.version)
    conn.close()