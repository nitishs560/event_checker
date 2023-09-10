from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('load_data', views.load_data, name='load_data')
]