from django.shortcuts import render, redirect
from . import oracleDB

from django.contrib.auth.models import User, Group

def index(request):
    return render(request, 'index.html')

def import_users(request):

    for user in User.objects.all():
        if user.groups.all()[0].name != 'admin':
            user.delete()

    def users_iterator():
        for fname, lname, mail, role in oracleDB.get_users(oracleDB.pool):
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