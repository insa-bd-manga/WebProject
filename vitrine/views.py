from datetime import datetime
from django.shortcuts import render, get_object_or_404

#pour les modèles
#from blog2.models import

#pour les formulaires
#from .forms import


def index(request):
    """l'index est la page d'accueil du site

    page compasée d'une descrption statique, puis des 3 derniers articles sortis

    :param request : OSEF
    :type request : requête HTTP

    :return paquet http contenant la page"""

    return render(request, 'vitrine/index.html')


def ouvrages(request):
    return 1


def festival(request):
    return 1


def archives(request):
    return 1


def infos(request):
    return 1


def contact(request):
    return 1
