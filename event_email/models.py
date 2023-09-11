from django.db import models
from datetime import date
from django.utils import timezone
# Create your models here.

class Event(models.Model):
    event_id = models.CharField(max_length=10)
    event_type = models.CharField(max_length=50)
    event_template = models.CharField(max_length=300)

    def __str__(self):
        return self.event_type

class EmployeeEmail(models.Model):
    employee_id = models.CharField(max_length=10)
    emp_name = models.CharField(max_length=50)
    email_id = models.CharField(max_length=50)

    def __str__(self):
        return self.employee_id

class EmpEvent(models.Model):
    employee_id = models.CharField(max_length=10)
    event_id = models.CharField(max_length=10)
    date = models.DateField()

    def __str__(self):
        return self.employee_id

class EventEmailStatus(models.Model):
    employee_email = models.CharField(max_length=50)
    event_type = models.CharField(max_length=50)
    event_message = models.CharField(max_length=300)
    email_status = models.CharField(max_length=10)
    email_error = models.CharField(max_length=300)
    execution_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.employee_email


class EventLog(models.Model):
    event_date = models.DateField(default=date.today)
    event_email_log = models.CharField(max_length=100)
    execution_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.event_date)


class SystemLog(models.Model):
    time_stamp = models.DateTimeField(default=timezone.now)
    system_status = models.CharField(max_length = 10)
    system_log = models.CharField(max_length=100)


    def __str__(self):
        return str(self.time_stamp)
