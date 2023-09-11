from django.shortcuts import render
from django.http import HttpResponse
from .models import Event
from .models import EmpEvent, EventLog
from .models import EmployeeEmail, EventEmailStatus, SystemLog
from smtplib import SMTPException
import pandas as pd
from datetime import date
from django.core.mail import EmailMessage
from IPython.display import HTML
from retry import retry


def home(request):
    """This function returns index page which gives access to other functionalities"""
    return render(request, 'index.html')

def event_data(request):
    """This function returns event table with different types of special occasions
    for which emails are sent on a schedule"""

    mydata = Event.objects.all().values()
    if mydata:
        df = pd.DataFrame(list(mydata))
        df = df.drop(['id'], axis=1)
        return HttpResponse(df.to_html(index=False))
    else:
        return HttpResponse("Event table containing types of event is empty.")

def employee_email(request):
    """Returns table of employees with their contact emails"""
    mydata = EmployeeEmail.objects.all().values()
    if mydata:
        df = pd.DataFrame(list(mydata))
        df = df.drop(['id'], axis=1)
        return HttpResponse(df.to_html(index=False))
    else:
        return HttpResponse("Employee email contact table is empty.")

def emp_event(request):
    """Returns table with events/special occasions for the employees in the organization"""
    mydata = EmpEvent.objects.all().values()
    if mydata:
        df = pd.DataFrame(list(mydata))
        df = df.drop(['id'], axis=1)
        return HttpResponse(df.to_html(index=False))
    else:
        return HttpResponse("Employee Events table is empty.")

def event_email_status(request):
    """Returns table with status of the email(Sent/Failed) being sent on special occasions to employees"""
    mydata = EventEmailStatus.objects.all().values()
    if mydata:
        df = pd.DataFrame(list(mydata))
        df = df.drop(['id'], axis=1)
        return HttpResponse(df.to_html(index=False))
    else:
        return HttpResponse("Event Email Status Table is empty.")

def event_log(request):
    """Returns table with the log of the daily event sending process"""
    mydata = EventLog.objects.all().values()
    if mydata:
        df = pd.DataFrame(list(mydata))
        df = df.drop(['id'], axis=1)
        return HttpResponse(df.to_html(index=False))
    else:
        return HttpResponse("Event Log is empty")

def system_log(request):
    """Returns table with log of any error encountered during email sending process not captured in event log"""
    mydata = SystemLog.objects.all().values()
    if mydata:
        df = pd.DataFrame(list(mydata))
        df = df.drop(['id'], axis=1)
        return HttpResponse(df.to_html(index=False))
    else:
        return HttpResponse("System Log is empty")


def load_event_data():
    """loads event data from the dataset event.csv to djangoDB"""
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
    """loads employee event data from the dataset emp_event.csv to djangoDB"""
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
    """loads employee email/contact data from the dataset emp_email.csv to djangoDB"""
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
    """Loads data to djangoDB from dataset/csvs if it is not already loaded"""
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
    return HttpResponse('Sample DATA has been loaded in SQLITE3 Django Database')

@retry(exceptions=SMTPException, tries=1, delay=3)
def prepare_mail(emp_email, emp_name, event, event_template):
    """Prepares email and sends respective event/special occasions email to employees"""
    try:
        message = event_template.replace('[Employee Name]', emp_name)
        message = message.replace('[Your Name]', "Data Axle Team")
        message = message.replace('[Company Name]', "Data Axle")
        message = message.replace("\\n", "\r\n")
        mail_subject = event
        to_email = emp_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        event_email_status = EventEmailStatus(employee_email=to_email, event_type=event, event_message=message,
                                              email_status="Sent", email_error="")
        event_email_status.save()
    except Exception as ex:
        print(ex)
        event_email_status = EventEmailStatus(employee_email=emp_email, event_type=event, event_message=event_template,
                                              email_status="Failed", email_error=ex)
        event_email_status.save()


def find_events():
    """Finds today's special occasions/events for the employees in the organization and
    initiates email sending process"""
    try:
        today = date.today()
        day, month = today.day, today.month
        try:
            event_latest_execution = EventEmailStatus.objects.filter(email_status = 'Sent').latest('execution_time').execution_time
            latest_day = event_latest_execution.day
            latest_month = event_latest_execution.month
        except Exception as ex:
            latest_day = day
            latest_month = month

        if (day >= latest_day) and (month >= latest_month):
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
                    prepare_mail(emp_email[0]['email_id'], emp_email[0]['emp_name'], event[0]['event_type'],
                                 event[0]['event_template'])
                    try:
                        today_sent_status = EventEmailStatus.objects.filter(employee_email=emp_email[0]['email_id'], event_type = event[0]['event_type'], email_status = 'Sent', execution_time__month=month, execution_time__day=day).values()
                    except Exception as ex:
                        today_sent_status = None
                    if emp_email and event and (not today_sent_status):
                        prepare_mail(emp_email[0]['email_id'], emp_email[0]['emp_name'], event[0]['event_type'],
                                     event[0]['event_template'])
        else:
            system_log = SystemLog(system_status='Ok', system_log="Emails have been sent already!")
            system_log.save()

    except Exception as ex:
        print("Error at find_events")
        system_log = SystemLog(system_status='Fail', system_log=ex)
        system_log.save()



