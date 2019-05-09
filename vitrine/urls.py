from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recherche-ouvrages', views.rechercheOuvrages, name='recherche-ouvrages'),
#   path('ouvrage/<str:auteur>/<str:titre>/<int:num_page>', views.ouvrage, name='ouvrage'),
    path('actus/<int:num_page>/<str:tag>', views.actus, name='actus'),
    path('article/<int:id_article>/<int:num_page>', views.article, name='article'),
    path('festival/<int:num_page>', views.festival, name='festival'),
    path('archives', views.archives, name='archives'),
    path('infos', views.infos, name='infos'),
    path('contact', views.contact, name='contact'),
]