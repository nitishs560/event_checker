from django.db import models

# Create your models here.

class Event(models.Model):
    event_id = models.CharField(max_length=10)
    event_type = models.CharField(max_length=50)
    event_template = models.CharField(max_length=300)

class EmployeeEmail(models.Model):
    employee_id = models.CharField(max_length=10)
    email_id = models.CharField(max_length=50)

class EmpEvent(models.Model):
    employee_id = models.CharField(max_length=10)
    event_id = models.CharField(max_length=10)
    date = models.DateField()


