from django.urls import path
from . import views

urlpatterns = [
    path('', views.testview, name='collector_tst'),
]