from django.shortcuts import render, redirect
from interface import oracleDB

from django.contrib.auth.models import Group
from .models import User

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

def display_table(request, cursor):
    query_header = [item[0] for item in cursor.description]
    query_result = []

    for item in cursor:
        query_result.append(item)

    return render(request, 'table_display.html', {'query_header': query_header, 'query_result' : query_result})

def tools(request):
    return display_table(request, oracleDB.get_tools(oracleDB.pool))

def researchers(request):
    return display_table(request, oracleDB.get_users(oracleDB.pool))

def experiments(request):
    return display_table(request, oracleDB.get_experiments(oracleDB.pool))

def results(request):
    return display_table(request, oracleDB.get_results(oracleDB.pool))

def about(request):
    return display_table(request, oracleDB.get_departments(oracleDB.pool))
