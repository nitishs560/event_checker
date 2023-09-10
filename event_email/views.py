from django.shortcuts import render
from django.http import HttpResponse
from .models import Event
from .models import EmpEvent
from .models import EmployeeEmail
# Create your views here.

def home(request):
    return HttpResponse("Hello World")

def load_data(request):
    return HttpResponse('Starting load data')