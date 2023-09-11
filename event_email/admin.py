from django.contrib import admin
from event_email.models import Event, EmpEvent, EmployeeEmail, EventEmailStatus, EventLog, SystemLog
# Register your models here.

admin.site.register(Event)
admin.site.register(EmpEvent)
admin.site.register(EmployeeEmail)
admin.site.register(EventEmailStatus)
admin.site.register(EventLog)
admin.site.register(SystemLog)