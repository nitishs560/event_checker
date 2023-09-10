from django.shortcuts import render
from django.http import HttpResponse
from .models import Event
from .models import EmpEvent
from .models import EmployeeEmail
# Create your views here.
import pandas as pd


def home(request):
    return HttpResponse("Hello World")

def load_event_data():
    try:
        event_df = pd.read_csv('./data_set/event.csv')
        for index, row in event_df.iterrows():
            event_model = Event(
                event_id=row['event_id'],
                event_type = row['event_type'],
                event_template = row['event_template']
            )
            event_model.save()
    except Exception as ex:
        print('Error Loading event table')
        print(ex)
    print("Completed Loading Event Table")

def load_emp_event_data():
    try:
        event_df = pd.read_csv('./data_set/emp_event.csv')
        for index, row in event_df.iterrows():
            emp_event_model = EmpEvent(
                employee_id=row['employee_id'],
                event_id = row['event_id'],
                date = row['date']
            )
            emp_event_model.save()
    except Exception as ex:
        print('Error Loading emp event table')
        print(ex)
    print("Completed Loading Employee Event Table")

def load_emp_email_data():
    try:
        event_df = pd.read_csv('./data_set/emp_email.csv')
        for index, row in event_df.iterrows():
            emp_contact_model = EmployeeEmail(
                employee_id=row['employee_id'],
                email_id = row['email_id']
            )
            emp_contact_model.save()
    except Exception as ex:
        print('Error Loading employee_email  table')
        print(ex)
    print("Completed Loading Employee Email Table")

def load_data(request):
    try:
        mydata = Event.objects.all().values()
        if not mydata:
            load_event_data()
        mydata = EmployeeEmail.objects.all().values()
        if not mydata:
            load_emp_email_data()
        mydata = EmpEvent.objects.all().values()
        if not mydata:
            load_emp_event_data()


    except Exception as ex:
        print("Caught in exception")
        print(ex)
    return HttpResponse('DATA IS IN DB NOW')