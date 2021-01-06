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

def email_in_use(pool, mail):
    csr = cursor(pool)
    csr.execute("""
        SELECT "UserID"
        FROM "Researchers"
        WHERE "Email Address" = '%s'
    """ % mail)
    csr.fetchall()
    res = csr.rowcount
    csr.close()
    return res != 0

def phone_in_use(pool, phone):
    csr = cursor(pool)
    csr.execute("""
        SELECT "UserID"
        FROM "Researchers"
        WHERE "Phone Number" = '%s'
    """ % phone)
    csr.fetchall()
    res = csr.rowcount
    csr.close()
    return res != 0

def get_user_by_id(pool, id):
    csr = cursor(pool)
    csr.execute("""
        SELECT "UserID", "First Name", "Last Name", "DepartmentID", "Email Address", "Phone Number", "Role" 
        FROM "Researchers"
        WHERE "UserID" = %d
    """ % int(id))
    return csr

def add_user(pool, fname, lname, deptID, email, phone, role):
    conn = pool.acquire()
    csr = conn.cursor()
    newest_id_wrapper = csr.var(cx_Oracle.NUMBER)
    sql_params = { "id_wrapper" : newest_id_wrapper }
    csr.execute("""
        INSERT INTO "Researchers"
        ("First Name", "Last Name", "DepartmentID", "Email Address", "Phone Number", "Role")
        VALUES
        ('%s', '%s', %d, '%s', '%s', '%s')
        RETURNING "UserID" into :id_wrapper
    """ % (fname, lname, int(deptID), email, phone, role), sql_params)
    conn.commit()

    return int(newest_id_wrapper.getvalue()[0])

def modify_user(pool, id, fname, lname, deptID, email, phone, rol):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        UPDATE "Researchers"
        SET "First Name" = '%s', "Last Name" = '%s', "DepartmentID" = '%d', "Email Address" = '%s', "Phone Number" = '%s', "Role" = '%s'
        WHERE "UserID" = %d
    """ % (fname, lname, int(deptID), email, phone, rol, int(id)))
    conn.commit()

def remove_user_by_id(pool, id):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        DELETE FROM "ExperimentsResearchersRelation"
        WHERE "UserID" = %d
    """ % int(id))
    csr.execute("""
        DELETE FROM "Researchers"
        WHERE "UserID" = %d
    """ % int(id))
    conn.commit()

def get_tools(pool):
    csr = cursor(pool)
    csr.execute("""
        SELECT t."ToolID" as "ID", t."Manufacturer", t."Model name", t."Serial Number", COALESCE(t."Specifications", '') "Specifications"
        FROM "Tools" t
        ORDER BY t."ToolID"
    """)
    return csr

def serial_number_in_use(pool, sn):
    csr = cursor(pool)
    csr.execute("""
        SELECT "ToolID"
        FROM "Tools"
        WHERE "Serial Number" = '%s'
    """ % sn)
    csr.fetchall()
    res = csr.rowcount
    csr.close()
    return res != 0

def get_tool_by_id(pool, id):
    csr = cursor(pool)
    csr.execute("""
        SELECT "ToolID", "Manufacturer", "Model name", "Serial Number", COALESCE("Specifications", '') "Specifications"
        FROM "Tools"
        WHERE "ToolID" = %d
    """ % int(id))
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

def modify_tool(pool, id, manufacturer, mname, sn, specs):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        UPDATE "Tools"
        SET "Manufacturer" = '%s', "Model name" = '%s', "Serial Number" = '%s', "Specifications" = '%s'
        WHERE "ToolID" = %d
    """ % (manufacturer, mname, sn, specs, int(id)))
    conn.commit()

def remove_tool_by_id(pool, id):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        DELETE FROM "ExperimentsToolsRelation"
        WHERE "ToolID" = %d
    """ % int(id))
    csr.execute("""
        DELETE FROM "Tools"
        WHERE "ToolID" = %d
    """ % int(id))
    conn.commit()

def get_experiments(pool):
    csr = cursor(pool)
    csr.execute("""
        SELECT e."ExperimentID" as "ID", e."Title", e."Description", e."Theory"
        FROM "Experiments" e
        ORDER BY e."ExperimentID"
    """)
    return csr

def get_experiments_full(pool):
    csr = cursor(pool)
    csr.execute("""
        SELECT e."ExperimentID" as "ID", e."Title", e."Description", e."Theory",
            (SELECT LISTAGG(r."First Name" || ' ' || r."Last Name", ', ') WITHIN GROUP (ORDER BY r."UserID")
            FROM "Researchers" r, "ExperimentsResearchersRelation" er
            WHERE r."UserID" = er."UserID" AND er."ExperimentID" = e."ExperimentID") AS "Researchers",
            (SELECT LISTAGG(t."Manufacturer" || ' ' || t."Model name", ', ') WITHIN GROUP (ORDER BY t."ToolID")
            FROM "Tools" t, "ExperimentsToolsRelation" et
            WHERE t."ToolID" = et."ToolID" AND et."ExperimentID" = e."ExperimentID") AS "Tools"
        FROM "Experiments" e
        ORDER BY e."ExperimentID"
    """)
    return csr

def get_experiment_by_id(pool, id):
    csr = cursor(pool)
    csr.execute("""
        SELECT "ExperimentID", "Title", "Description", "Theory"
        FROM "Experiments"
        WHERE "ExperimentID" = %d
    """ % int(id))
    return csr

def get_users_from_experiment(pool, id):
    csr = cursor(pool)
    csr.execute("""
        SELECT "UserID"
        FROM "ExperimentsResearchersRelation"
        WHERE "ExperimentID" = %d
    """ % int(id))
    return csr

def get_tools_from_experiment(pool, id):
    csr = cursor(pool)
    csr.execute("""
        SELECT "ToolID"
        FROM "ExperimentsToolsRelation"
        WHERE "ExperimentID" = %d
    """ % int(id))
    return csr

def _add_researchers_to_experiment(csr, id, researchers):
    for userID in researchers:
        csr.execute("""
            INSERT INTO "ExperimentsResearchersRelation"
            ("ExperimentID", "UserID")
            VALUES
            ('%d', %d)
        """ % (int(id), int(userID)))

def _add_tools_to_experiment(csr, id, tools):
    for toolID in tools:
        csr.execute("""
            INSERT INTO "ExperimentsToolsRelation"
            ("ExperimentID", "ToolID")
            VALUES
            ('%d', %d)
        """ % (int(id), int(toolID)))
        
def add_experiment(pool, title, desc, theory, researchers, tools):
    conn = pool.acquire()
    csr = conn.cursor()
    newest_id_wrapper = csr.var(cx_Oracle.NUMBER)
    sql_params = { "id_wrapper" : newest_id_wrapper }
    csr.execute("""
        INSERT INTO "Experiments"
        ("Title", "Description", "Theory")
        VALUES
        ('%s', '%s', '%s')
        RETURNING "ExperimentID" into :id_wrapper
    """ % (title, desc, theory), sql_params)
    id = newest_id_wrapper.getvalue()[0]

    _add_researchers_to_experiment(csr, id, researchers)
    _add_tools_to_experiment(csr, id, tools)

    conn.commit()

def modify_experiment(pool, id, title, desc, theory, researchers, tools):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        UPDATE "Experiments"
        SET "Title" = '%s', "Description" = '%s', "Theory" = '%s'
        WHERE "ExperimentID" = %d
    """ % (title, desc, theory, int(id)))

    csr.execute("""
        DELETE FROM "ExperimentsResearchersRelation"
        WHERE "ExperimentID" = %d
    """ % int(id))

    _add_researchers_to_experiment(csr, id, researchers)

    csr.execute("""
        DELETE FROM "ExperimentsToolsRelation"
        WHERE "ExperimentID" = %d
    """ % int(id))

    _add_tools_to_experiment(csr, id, tools)

    conn.commit()

def remove_experiment_by_id(pool, id):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        DELETE FROM "ExperimentsResearchersRelation"
        WHERE "ExperimentID" = %d
    """ % int(id))
    csr.execute("""
        DELETE FROM "ExperimentsToolsRelation"
        WHERE "ExperimentID" = %d
    """ % int(id))
    csr.execute("""
        DELETE FROM "Results"
        WHERE "ExperimentID" = %d
    """ % int(id))
    csr.execute("""
        DELETE FROM "Experiments"
        WHERE "ExperimentID" = %d
    """ % int(id))
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

def get_result_by_id(pool, id):
    csr = cursor(pool)
    csr.execute("""
        SELECT "ResultID", "ExperimentID", "Remarks", "Observations", "Description"
        FROM "Results"
        WHERE "ResultID" = %d
    """ % int(id))
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

def modify_result(pool, id, experiment, remarks, obs, desc):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        UPDATE "Results"
        SET "ExperimentID" = %d, "Remarks" = '%s', "Observations" = '%s', "Description" = '%s'
        WHERE "ResultID" = %d
    """ % (int(experiment), remarks, obs, desc, int(id)))
    conn.commit()

def remove_result_by_id(pool, id):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        DELETE FROM "Results"
        WHERE "ResultID" = %d
    """ % int(id))
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

def get_department_by_id(pool, id):
    csr = cursor(pool)
    csr.execute("""
        SELECT *
        FROM "Departments"
        WHERE "DepartmentID" = %d
    """ % int(id))
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

def modify_department(pool, id, dname, bID, web):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        UPDATE "Departments"
        SET "Department Name" = '%s', "BuildingID" = %d, "Website" = '%s'
        WHERE "DepartmentID" = %d
    """ % (dname, int(bID), web, int(id)))
    conn.commit()

def remove_department_by_id(pool, id):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        DELETE FROM "Departments"
        WHERE "DepartmentID" = %d
    """ % int(id))
    conn.commit()

def get_buildings(pool):
    csr = cursor(pool)
    csr.execute('SELECT * FROM "Buildings"')
    return csr

def get_building_by_id(pool, id):
    csr = cursor(pool)
    csr.execute("""
        SELECT *
        FROM "Buildings"
        WHERE "BuildingID" = %d
    """ % int(id))
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

def modify_building(pool, id, address, city, zipcode):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        UPDATE "Buildings"
        SET "Address" = '%s', "City" = '%s', "Zipcode" = '%s'
        WHERE "BuildingID" = %d
    """ % (address,city, zipcode, int(id)))
    conn.commit()


def get_buildings_no_dept(pool, id = -1):
    csr = cursor(pool)
    if id == -1:
        csr.execute("""
            SELECT "BuildingID", "Address", "City", "Zipcode" 
            FROM "Buildings"
            WHERE "BuildingID" NOT IN (
                SELECT "BuildingID" 
                FROM "Departments"
                )
        """)
    else:
        csr.execute("""
            SELECT "BuildingID", "Address", "City", "Zipcode" 
            FROM "Buildings"
            WHERE "BuildingID" NOT IN (
                SELECT "BuildingID" 
                FROM "Departments"
                WHERE "DepartmentID" != %d
                )
        """ % int(id))
    return csr

def remove_building_by_id(pool, id):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        DELETE FROM "Departments"
        WHERE "BuildingID" = %d
    """ % int(id))
    csr.execute("""
        DELETE FROM "Buildings"
        WHERE "BuildingID" = %d
    """ % int(id))
    conn.commit()

def remove_building_and_dept_by_id(pool, id):
    conn = pool.acquire()
    csr = conn.cursor()
    csr.execute("""
        SELECT "BuildingID"
        FROM "Departments"
        WHERE "DepartmentID" = %d
    """ % int(id))
    bid = csr.fetchone()
    csr.execute("""
        DELETE FROM "Departments"
        WHERE "DepartmentID" = %d
    """ % int(id))
    csr.execute("""
        DELETE FROM "Buildings"
        WHERE "BuildingID" = %d
    """ % int(bid))
    conn.commit()

print("Connecting to database...")
pool = connect()
print("Database version:", pool.acquire().version)