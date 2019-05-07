from datetime import datetime
from django.shortcuts import render, get_object_or_404

#pour les modèles
from vitrine.models import Article, Commentaire, Tag

#pour les formulaires
#from .forms import


def index(request):
    """l'index est la page d'accueil du site

    page composée d'une description statique, puis des 3 derniers articles sortis

    :param request : OSEF
    :type request : requête HTTP

    :return paquet http contenant la page"""

    # récupération des 3 derniers articles
    query = Article.objects.all().order_by("-date")[:3]

    return render(request, 'vitrine/index.html', {"last_articles": query})


def ouvrages(request):
    return 1


def festival(request):
    """page sur le festival et le concours BD

        page composée d'une description statique, puis des articles tagués "festival" et "concours"

        :param request : OSEF
        :type request : requête HTTP

        :return paquet http contenant la page"""
    return 1


def archives(request):
    return 1


def infos(request):
    return 1


def contact(request):
    return 1
