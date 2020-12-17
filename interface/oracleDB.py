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
    csr.execute("""
        SELECT r."UserID" as "ID", r."First Name", r."Last Name", d."Department Name" as "Department", r."Email Address", r."Phone Number", r."Role" 
        FROM "Researchers" r, "Departments" d
        WHERE r."DepartmentID" = d."DepartmentID"
        ORDER BY r."UserID"
    """)
    return csr

def get_tools(pool):
    csr = cursor(pool)
    csr.execute("""
        SELECT t."ToolID" as "ID", t."Manufacturer", t."Model name", t."Serial Number", COALESCE(t."Specifications", '') "Specifications"
        FROM "Tools" t
        ORDER BY t."ToolID"
    """)
    return csr

def get_experiments(pool):
    csr = cursor(pool)
    csr.execute("""
        SELECT e."ExperimentID" as "ID", e."Title", e."Description", e."Theory"
        FROM "Experiments" e
        ORDER BY e."ExperimentID"
    """)
    return csr

def get_results(pool):
    csr = cursor(pool)
    csr.execute("""
        SELECT r."ResultID" as "ID", e."Title" as "Experiment", r."Remarks", r."Observations", r."Description"
        FROM "Results" r, "Experiments" e
        WHERE r."ExperimentID" = e."ExperimentID"
        ORDER BY r."ResultID"
    """)
    return csr

def get_departments(pool):
    csr = cursor(pool)
    csr.execute("""
        SELECT d."DepartmentID" as "ID", d."Department Name", b."Address" || ' ' || b."City" || ' ' || b."Zipcode" "Address", COALESCE(d."Website", '') "Website"
        FROM "Departments" d, "Buildings" b
        WHERE d."BuildingID" = b."BuildingID"
        ORDER BY d."DepartmentID"
    """)
    return csr

def get_buildings(pool):
    csr = cursor(pool)
    csr.execute('SELECT * FROM "Buildings"')
    return csr

pool = connect()
print("Database version:", pool.acquire().version)