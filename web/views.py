from django.shortcuts import render, redirect
from interface import oracleDB

from django.contrib.auth.models import Group
from .models import User
from .forms import *

from functools import partial

def index(request):
    return render(request, 'index.html')

def import_users(request):

    for user in User.objects.all():
        if user.groups.all()[0].name != 'admin':
            user.delete()

    def users_iterator():
        for _, fname, lname, _, mail, _, role in oracleDB.get_users(oracleDB.pool):
            user = User.objects.create(
                username=mail.split('@')[0],
                first_name=fname,
                last_name=lname,
                email=mail
            )
            user.set_password(fname + lname)
            group = Group.objects.get(name=role) 
            group.user_set.add(user)
            user.save()
            group.save()
            yield user

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

    return render(request, 'table_display.html', {'query_header': query_header, 'query_result' : query_result, 'table_name' : table_name})

### DISPLAY ###

def display_tools(request):
    return display_table(request, oracleDB.get_tools(oracleDB.pool), 'Tools')

def display_researchers(request):
    return display_table(request, oracleDB.get_users(oracleDB.pool), 'Researchers')

def display_experiments(request):
    return display_table(request, oracleDB.get_experiments(oracleDB.pool), 'Experiments')

def display_results(request):
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
        #TODO: db_processor
        pass

    return form_wrapper(request, AddToolForm, 'Tool', '/tools', db_processor)

def add_researcher(request):
    def db_processor(form):
        #TODO: db_processor
        pass

    return form_wrapper(request, partial(AddResearcherForm, db_pool=oracleDB.pool), 'Researcher', '/researchers', db_processor)

def add_experiment(request):
    def db_processor(form):
        #TODO: db_processor
        pass

    return form_wrapper(request, partial(AddExperimentForm, db_pool=oracleDB.pool), 'Experiment', '/experiments', db_processor)

def add_result(request):
    def db_processor(form):
        #TODO: db_processor
        pass

    return form_wrapper(request, partial(AddResultForm, db_pool=oracleDB.pool), 'Result', '/results', db_processor)

def add_basic(request):
    def db_processor_building(form):
        #TODO: db_processor
        pass
    def db_processor_dept(form):
        #TODO: db_processor
        pass
    
    return form_wrapper(request, (AddBuildingForm, partial(AddDepartmentForm, db_pool=oracleDB.pool)), \
                        ('Building', 'Department'), ('/about', '/about'), (db_processor_building, db_processor_dept))
