from django.shortcuts import render
from django.http import HttpResponse
from .models import Event
from .models import EmpEvent, EventLog
from .models import EmployeeEmail, EventEmailStatus, SystemLog
# Create your views here.
import pandas as pd
from datetime import date
from django.core.mail import EmailMessage

def home(request):
    return HttpResponse("Hello World")

def load_event_data():
    try:
        event_df = pd.read_csv('./data_set/event.csv', sep='|')
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
                emp_name=row['emp_name'],
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
    find_events()
    return HttpResponse('DATA IS IN DB NOW')

def prepare_mail(emp_email, emp_name, event, event_template):
    try:
        message = event_template.replace('[Employee Name]', emp_name)
        message = message.replace('[Your Name]', "Data Axle Team")
        message = message.replace('[Company Name]', "Data Axle")
        message = message.replace("\\n", "\r\n")
        print(message)
        mail_subject = event
        to_email = emp_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        # email.send()
        event_email_status = EventEmailStatus(employee_email=to_email, event_type=event, event_message=message,
                                              email_status="Sent", email_error="")
        event_email_status.save()
    except Exception as ex:
        print(ex)
        event_email_status = EventEmailStatus(employee_email=emp_email, event_type=event, event_message=event_template,
                                              email_status="Failed", email_error=ex)
        event_email_status.save()


def find_events():
    try:
        today = date.today()
        day, month = today.day, today.month
        # event_email_status = EventEmailStatus.objects.filter(execution_time__month=month, execution_time__day=day).values()execution_time
        event_latest_execution = EventEmailStatus.objects.filter(email_status = 'Sent').latest('execution_time').execution_time

        if (day < event_latest_execution.day) and (month < event_latest_execution.month):
            system_log = SystemLog(system_status='Ok', system_log="Emails have been sent already!")
            system_log.save()
        else:
            emp_event = EmpEvent.objects.filter(date__month=month, date__day=day).values()
            if not emp_event:
                event_log = EventLog(event_email_log="no events are scheduled for the current period")
                event_log.save()
            else:
                event_log = EventLog(event_email_log="Events email sending process initiated")
                event_log.save()
                for i in emp_event:
                    emp_email = EmployeeEmail.objects.filter(employee_id=i['employee_id']).values()
                    event = Event.objects.filter(event_id=i['event_id']).values()
                    if emp_email and event:
                        prepare_mail(emp_email[0]['email_id'], emp_email[0]['emp_name'], event[0]['event_type'], event[0]['event_template'])
    except Exception as ex:
        print("Error at find_events")
        system_log = SystemLog(system_status='Fail', system_log=ex)
        system_log.save()



