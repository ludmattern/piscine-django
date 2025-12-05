from django.urls import path
from . import views

app_name = 'ex03'

urlpatterns = [
    path('', views.index, name='index'),
]
