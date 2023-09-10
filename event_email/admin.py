from django.contrib import admin
from event_email.models import Event, EmpEvent, EmployeeEmail
# Register your models here.

admin.site.register(Event)
admin.site.register(EmpEvent)
admin.site.register(EmployeeEmail)