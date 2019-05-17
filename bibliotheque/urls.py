from django.urls import path
from . import views

urlpatterns = [
    path('recherche', views.recherche, name='recherche'),
    path('recherche/<int:num_page>', views.recherche, name='recherche')
]
