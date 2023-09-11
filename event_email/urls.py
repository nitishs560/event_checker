from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('load_data', views.load_data, name='load_data'),
    path('event_data', views.event_data, name='event_data'),
    path('emp_event', views.emp_event, name='emp_event'),
    path('employee_email', views.employee_email, name='employee_email'),
    path('event_email_status', views.event_email_status, name='event_email_status'),
    path('event_log', views.event_log, name='event_log'),
    path('system_log', views.system_log, name='system_log'),
]