from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ouvrages', views.ouvrages, name='ouvrages'),
    path('festival', views.festival, name='festival'),
    path('archives', views.archives, name='archives'),
    path('infos', views.infos, name='infos'),
    path('contact', views.contact, name='contact'),
]