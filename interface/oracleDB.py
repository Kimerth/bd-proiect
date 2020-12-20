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

def add_user(pool, fname, lname, deptID, email, phone, role):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        INSERT INTO "Researchers"
        ("First Name", "Last Name", "DepartmentID", "Email Address", "Phone Number", "Role")
        VALUES
        ('%s', '%s', %d, '%s', '%s', '%s')
    """ % (fname, lname, int(deptID), email, phone, role))
    conn.commit()

def get_tools(pool):
    csr = cursor(pool)
    csr.execute("""
        SELECT t."ToolID" as "ID", t."Manufacturer", t."Model name", t."Serial Number", COALESCE(t."Specifications", '') "Specifications"
        FROM "Tools" t
        ORDER BY t."ToolID"
    """)
    return csr

def add_tool(pool, manufacturer, mname, sn, specs):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        INSERT INTO "Tools"
        ("Manufacturer", "Model name", "Serial Number", "Specifications")
        VALUES
        ('%s', '%s', '%s', '%s')
    """ % (manufacturer, mname, sn, specs))
    conn.commit()

def get_experiments(pool):
    csr = cursor(pool)
    csr.execute("""
        SELECT e."ExperimentID" as "ID", e."Title", e."Description", e."Theory"
        FROM "Experiments" e
        ORDER BY e."ExperimentID"
    """)
    return csr

def add_experiment(pool, title, desc, theory):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        INSERT INTO "Experiments"
        ("Title", "Description", "Theory")
        VALUES
        ('%s', '%s', '%s')
    """ % (title, desc, theory))
    conn.commit()

def get_results(pool):
    csr = cursor(pool)
    csr.execute("""
        SELECT r."ResultID" as "ID", e."Title" as "Experiment", r."Remarks", r."Observations", r."Description"
        FROM "Results" r, "Experiments" e
        WHERE r."ExperimentID" = e."ExperimentID"
        ORDER BY r."ResultID"
    """)
    return csr

def add_result(pool, experiment, remarks, obs, desc):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        INSERT INTO "Results"
        ("ExperimentID", "Remarks", "Observations", "Description")
        VALUES
        (%d, '%s', '%s', '%s')
    """ % (int(experiment), remarks, obs, desc))
    conn.commit()

def get_departments(pool):
    csr = cursor(pool)
    csr.execute("""
        SELECT d."DepartmentID" as "ID", d."Department Name", b."Address" || ' ' || b."City" || ' ' || b."Zipcode" "Address", COALESCE(d."Website", '') "Website"
        FROM "Departments" d, "Buildings" b
        WHERE d."BuildingID" = b."BuildingID"
        ORDER BY d."DepartmentID"
    """)
    return csr

def add_department(pool, dname, bID, web):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        INSERT INTO "Departments"
        ("Department Name", "BuildingID", "Website")
        VALUES
        ('%s', %d, '%s')
    """ % (dname, int(bID), web))
    conn.commit()

def get_buildings(pool):
    csr = cursor(pool)
    csr.execute('SELECT * FROM "Buildings"')
    return csr

def add_building(pool, address, city, zipcode):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        INSERT INTO "Buildings"
        ("Address", "City", "Zipcode")
        VALUES
        ('%s', '%s', '%s')
    """ % (address, city, zipcode))
    conn.commit()

def get_buildings_no_dept(pool):
    csr = cursor(pool)
    csr.execute("""
        SELECT "BuildingID", "Address", "City", "Zipcode" FROM "Buildings"
        WHERE "BuildingID" NOT IN (SELECT "BuildingID" FROM "Departments")
    """)
    return csr

pool = connect()
print("Database version:", pool.acquire().version)