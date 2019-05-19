from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recherche-ouvrages', views.rechercheOuvrages, name='recherche-ouvrages'),

#   path('ouvrage/<str:auteur>/<str:titre>/<int:num_page>', views.ouvrage, name='ouvrage'),

    path('actus/<str:tag>/<int:num_page>', views.actus, name='actus'),
    path('actus/<str:tag>', views.actus, name='actus'),
    path('actus/<int:num_page>', views.actus, name='actus'),
    path('actus/', views.actus, name='actus'),

    path('article/<int:id_article>/<int:page_commentaire>', views.article, name='article'),
    path('article/<int:id_article>', views.article, name='article'),
    path('article', views.article, name='article'),

    path('festival/<int:num_page>', views.festival, name='festival'),
    path('festival', views.festival, name='festival'),



    # path('archives/<str:tag>/<int:year>/<int:month>/<int:num_page>', views.archives, name='archives'),
    # path('archives/<str:tag>/<int:year>', views.archives, name='archives'),
    # path('archives/<int:year>/<int:month>', views.archives, name='archives'),
    # path('archives/<int:year>', views.archives, name='archives'),
    # path('archives/<int:month>', views.archives, name='archives'),
    # path('archives/<str:tag>', views.archives, name='archives'),
    path('archives', views.archives, name='archives'),
    path('archives/<int:num_page>', views.archives, name='archives'),
    # path('archives/<str:tag>/<int:year>/<int:num_page>', views.archives, name='archives'),
    # path('archives/<int:year>/<int:month>/<int:num_page>', views.archives, name='archives'),
    # path('archives/<int:year>/<int:num_page>', views.archives, name='archives'),
    # path('archives/<int:month>/<int:num_page>', views.archives, name='archives'),
    # path('archives/<str:tag>/<int:num_page>', views.archives, name='archives'),
    # path('archives/<int:num_page>', views.archives, name='archives'),

    path('infos', views.infos, name='infos'),
    path('contact', views.contact, name='contact'),
]