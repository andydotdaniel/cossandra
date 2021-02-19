from django.urls import path

from . import views

app_name = 'traces'
urlpatterns = [
    path('', views.index, name='index'),
    path('entry', views.entry, name='entry'),
]