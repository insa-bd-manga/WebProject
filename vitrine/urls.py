from django.urls import path
from . import views
from bibliotheque import views as biblio_views

urlpatterns = [
    path('', views.index, name='index'),

    path('recherche-ouvrages', biblio_views.recherche, name='recherche-ouvrages'),

    path('actus/<str:tag>/<int:num_page>', views.actus, name='actus'),
    path('actus/<int:num_page>', views.actus, name='actus'),
    path('actus/<str:tag>', views.actus, name='actus'),
    path('actus/', views.actus, name='actus'),

    path('article/<int:id_article>/<int:page_commentaire>', views.article, name='article'),
    path('article/<int:id_article>', views.article, name='article'),
    path('article', views.article, name='article'),

    path('festival', views.festival, name='festival'),
    path('festival/<int:num_page>', views.festival, name='festival'),

    path('archives', views.archives, name='archives'),
    path('archives/<int:num_page>', views.archives, name='archives'),

    path('infos', views.infos, name='infos'),

    path('contact', views.contact, name='contact'),

    path('documentation', views.doc, name='doc'),
]