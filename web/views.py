from django.shortcuts import render, redirect
from interface import oracleDB

from django.contrib.auth.models import Group
from .models import User
from .forms import *

from functools import partial

def create_user(id, fname, lname, mail, role):
    user = User.objects.create(
        username=mail.split('@')[0],
        first_name=fname,
        last_name=lname,
        email=mail,
        uid = id
    )
    user.set_password(fname + lname)
    group = Group.objects.get(name=role) 
    group.user_set.add(user)
    user.save()
    group.save()

def index(request):
    return render(request, 'index.html')

def import_users(request):
    for user in User.objects.all():
        if user.groups.all()[0].name != 'admin':
            user.delete()

    def users_iterator():
        for id, fname, lname, _, mail, _, role in oracleDB.get_users(oracleDB.pool):
            yield create_user(id, fname, lname, mail, role)

    try:
        User.objects.bulk_create(iter(users_iterator()))
    except:
        pass

    return redirect('/admin')

def display_table(request, cursor, table_name):
    query_header = [item[0] for item in cursor.description]
    query_result = cursor.fetchall()
    cursor.close()
    return render(request, 'table_display.html', {'query_header': query_header, 'query_result' : query_result, 'table_name' : table_name})

### DISPLAY ###

def display_tools(request):
    if request.method == 'POST':
        if 'remove' in request.POST:
            oracleDB.remove_tool_by_id(oracleDB.pool, request.POST['remove'])
    return display_table(request, oracleDB.get_tools(oracleDB.pool), 'Tools')

def display_researchers(request):
    if request.method == 'POST':
        if 'remove' in request.POST:
            oracleDB.remove_user_by_id(oracleDB.pool, request.POST['remove'])
            u = User.objects.get(uid = request.POST['remove'])
            u.delete()

    return display_table(request, oracleDB.get_users(oracleDB.pool), 'Researchers')

def display_experiments(request):
    if request.method == 'POST':
        if 'remove' in request.POST:
            oracleDB.remove_experiment_by_id(oracleDB.pool, request.POST['remove'])

    query_result = []
    with oracleDB.get_experiments(oracleDB.pool) as csr:
        query_header = [item[0] for item in csr.description]
        query_header.extend(['Researchers', 'Tools'])
        for id, title, description, theory in csr:
            with oracleDB.get_users_from_experiment(oracleDB.pool, id) as csr2:
                researchers = []
                for userID in csr2:
                    with oracleDB.get_user_by_id(oracleDB.pool, *userID) as csr3:
                        for _, fname, lname, _, _, _, _ in csr3:
                            researchers.append("%s %s" % (fname, lname))
            researchers = ', '.join(researchers)

            with oracleDB.get_tools_from_experiment(oracleDB.pool, id) as csr2:
                tools = []
                for toolID in csr2:
                    with oracleDB.get_tool_by_id(oracleDB.pool, *toolID) as csr3:
                        for _, manufacturer, mname, _, _ in csr3:
                            tools.append("%s %s" % (manufacturer, mname))
            tools = ', '.join(tools)

            query_result.append((id, title, description, theory, researchers, tools))
    
    return render(request, 'table_display.html', {'query_header': query_header, 'query_result' : query_result, 'table_name' : 'Experiments'})

def display_results(request):
    if request.method == 'POST':
        if 'remove' in request.POST:
            oracleDB.remove_result_by_id(oracleDB.pool, request.POST['remove'])
    return display_table(request, oracleDB.get_results(oracleDB.pool), 'Results')

def display_about(request):
    return display_table(request, oracleDB.get_departments(oracleDB.pool), 'About')

### ADD ###

def form_wrapper(request, form_class, item_name, parent, db_processor, form_creation_cb = None):
    if type(form_class) is tuple:
        fc1, fc2 = form_class
        in1, in2 = item_name
        p1, p2 = parent
        dbp1, dbp2 = db_processor
        if request.method == 'POST':
            form1 = fc1(data=request.POST)
            if form1.is_valid():
                dbp1(form1)
                return redirect(p1)
        else:
            form1 = fc1()

        if request.method == 'POST' and not form1.is_valid():
            form2 = fc2(data=request.POST)
            if form2.is_valid():
                dbp2(form2)
                return redirect(p2)
        else:
            form2 = fc2()

        return render(request, 'add_entry.html', {'form': form1, 'form2': form2, 'item_name': in1, 'item2_name': in2})
                
    else:
        if request.method == 'POST':
            form = form_class(data=request.POST)
            if form.is_valid():
                db_processor(form)
                return redirect(parent)
        else:
            if not form_creation_cb:
                form = form_class()
            else:
                form = form_creation_cb(form_class())

        return render(request, 'add_entry.html', {'form': form, 'item_name' : item_name})

def db_processor_tool(form, id = 0):
    manufacturer = form.cleaned_data['manufacturer']
    mname = form.cleaned_data['model_name']
    sn = form.cleaned_data['serial_number']
    specs = form.cleaned_data['specifications']

    if id == 0:
        oracleDB.add_tool(oracleDB.pool, manufacturer, mname, sn, specs)
    else:
        oracleDB.modify_tool(oracleDB.pool, id, manufacturer, mname, sn, specs)

def db_processor_researcher(form):
    fname = form.cleaned_data['first_name']
    lname = form.cleaned_data['last_name']
    mail = form.cleaned_data['email']
    phone = form.cleaned_data['phone']
    dept = form.cleaned_data['department']
    role = form.cleaned_data['role']

    id = oracleDB.add_user(oracleDB.pool, fname, lname, dept, mail, phone, role)

    create_user(id, fname, lname, mail, role)

def db_processor_experiment(form):
    title = form.cleaned_data['title']
    desc = form.cleaned_data['description']
    theory = form.cleaned_data['theory']
    researchers = form.cleaned_data['researchers']
    tools = form.cleaned_data['tools']

    oracleDB.add_experiment(pool, title, desc, theory, researchers, tools)

def db_processor_result(form):
    experiment = form.cleaned_data['experiment']
    remarks = form.cleaned_data['remarks']
    obs = form.cleaned_data['observations']
    desc = form.cleaned_data['description']

    oracleDB.add_result(oracleDB.pool, experiment, remarks, obs, desc)

def db_processor_building(form):
    address = form.cleaned_data['address']
    city = form.cleaned_data['city']
    zipcode = form.cleaned_data['zipcode']
    
    oracleDB.add_building(oracleDB.pool, address, city, zipcode)

def db_processor_dept(form):
    dname = form.cleaned_data['department_name']
    bID = form.cleaned_data['building']
    web = form.cleaned_data['website']

    oracleDB.add_department(oracleDB.pool, dname, bID, web)

def add_tool(request):
    return form_wrapper(request, AddToolForm, 'Tool', '/tools', db_processor_tool)

def add_researcher(request):
    return form_wrapper(request, partial(AddResearcherForm, db_pool=oracleDB.pool), 'Researcher', '/researchers', db_processor_researcher)

def add_experiment(request):
    return form_wrapper(request, partial(AddExperimentForm, db_pool=oracleDB.pool), 'Experiment', '/experiments', db_processor_experiment)

def add_result(request):
    return form_wrapper(request, partial(AddResultForm, db_pool=oracleDB.pool), 'Result', '/results', db_processor_result)

def add_basic(request):
    return form_wrapper(request, (AddBuildingForm, partial(AddDepartmentForm, db_pool=oracleDB.pool)), \
                        ('Building', 'Department'), ('/about', '/about'), (db_processor_building, db_processor_dept))

### MODIFY ###

def get_id(request):
    if request.method == 'POST' and 'edit' in request.POST:
        request.method = 'GET'
        id = request.POST['edit']
        request.session['id'] = id
    else:
        id = request.session['id']

    return id

def modify_tool(request):
    id = get_id(request)

    def populate_form(form):
        with oracleDB.get_tool_by_id(oracleDB.pool, id) as csr:
            _, form.initial['manufacturer'], form.initial['model_name'], form.initial['serial_number'], form.initial['specifications'] = csr.fetchone()
        return form

    return form_wrapper(request, AddToolForm, 'Tool', '/tools', partial(db_processor_tool, id=id), populate_form)

def modify_researcher(request):
    id = get_id(request)

    def populate_form(form):
        with oracleDB.get_user_by_id(oracleDB.pool, id) as csr:
            _, form.initial['first_name'], form.initial['last_name'], \
                form.initial['department'], form.initial['email'], form.initial['phone'], form.initial['role'] = csr.fetchone()
        return form

    return form_wrapper(request, partial(AddResearcherForm, db_pool=oracleDB.pool), 'Researcher', '/researchers', \
        partial(db_processor_researcher, id=id), populate_form)

def modify_experiment(request):
    id = get_id(request)

    def populate_form(form):
        with oracleDB.get_experiment_by_id(oracleDB.pool, id) as csr:
            _, form.initial['title'], form.initial['description'], form.initial['theory'] = csr.fetchone()

        with oracleDB.get_users_from_experiment(oracleDB.pool, id) as csr:
            researchers = []
            for x in csr:
                researchers.append(*x)
        form.initial['researchers'] = researchers

        with oracleDB.get_tools_from_experiment(oracleDB.pool, id) as csr:
            tools = []
            for x in csr:
                tools.append(*x)
        form.initial['tools'] = tools

        return form

    return form_wrapper(request, partial(AddExperimentForm, db_pool=oracleDB.pool), 'Experiment', '/experiments', \
        partial(db_processor_experiment, id=id), populate_form)

def modify_result(request):
    id = get_id(request)

    return form_wrapper(request, partial(AddResultForm, db_pool=oracleDB.pool), 'Result', '/results', db_processor_result)

def modify_basic(request):
    id = get_id(request)

    return form_wrapper(request, (AddBuildingForm, partial(AddDepartmentForm, db_pool=oracleDB.pool)), \
                        ('Building', 'Department'), ('/about', '/about'), (db_processor_building, db_processor_dept))