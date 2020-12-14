from django.shortcuts import render
from . import oracleDB

def index(request):
    return render(request, 'index.html')