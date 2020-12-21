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
    query_result = []

    for item in cursor:
        query_result.append(item)

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
    return display_table(request, oracleDB.get_experiments(oracleDB.pool), 'Experiments')

def display_results(request):
    if request.method == 'POST':
        if 'remove' in request.POST:
            oracleDB.remove_result_by_id(oracleDB.pool, request.POST['remove'])
    return display_table(request, oracleDB.get_results(oracleDB.pool), 'Results')

def display_about(request):
    return display_table(request, oracleDB.get_departments(oracleDB.pool), 'About')

### ADD ###

def form_wrapper(request, form_class, item_name, parent, db_processor):
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
            form = form_class()

        return render(request, 'add_entry.html', {'form': form, 'item_name' : item_name})

def add_tool(request):
    def db_processor(form):
        manufacturer = form.cleaned_data['manufacturer']
        mname = form.cleaned_data['model_name']
        sn = form.cleaned_data['serial_number']
        specs = form.cleaned_data['specifications']

        oracleDB.add_tool(oracleDB.pool, manufacturer, mname, sn, specs)

    return form_wrapper(request, AddToolForm, 'Tool', '/tools', db_processor)

def add_researcher(request):
    def db_processor(form):
        fname = form.cleaned_data['first_name']
        lname = form.cleaned_data['last_name']
        mail = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        dept = form.cleaned_data['department']
        role = form.cleaned_data['role']

        id = oracleDB.add_user(oracleDB.pool, fname, lname, dept, mail, phone, role)
        create_user(id, fname, lname, mail, role)

    return form_wrapper(request, partial(AddResearcherForm, db_pool=oracleDB.pool), 'Researcher', '/researchers', db_processor)

def add_experiment(request):
    def db_processor(form):
        title = form.cleaned_data['title']
        desc = form.cleaned_data['description']
        theory = form.cleaned_data['theory']

        oracleDB.add_experiment(pool, title, desc, theory)

    return form_wrapper(request, partial(AddExperimentForm, db_pool=oracleDB.pool), 'Experiment', '/experiments', db_processor)

def add_result(request):
    def db_processor(form):
        experiment = form.cleaned_data['experiment']
        remarks = form.cleaned_data['remarks']
        obs = form.cleaned_data['observations']
        desc = form.cleaned_data['description']

        oracleDB.add_result(oracleDB.pool, experiment, remarks, obs, desc)

    return form_wrapper(request, partial(AddResultForm, db_pool=oracleDB.pool), 'Result', '/results', db_processor)

def add_basic(request):
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
    
    return form_wrapper(request, (AddBuildingForm, partial(AddDepartmentForm, db_pool=oracleDB.pool)), \
                        ('Building', 'Department'), ('/about', '/about'), (db_processor_building, db_processor_dept))
