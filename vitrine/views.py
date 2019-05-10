from datetime import datetime
from django.shortcuts import render, get_object_or_404

#pour les modèles
from vitrine.models import Article, Commentaire, Tag

#Pour des query plus complexes que le set de base
from django.db.models import Q

#Pour la data
from django.utils import timezone

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


def rechercheOuvrages(request):
    """Page de recherche d'ouvrage par nom/auteur

    :param request : OSEF
    :type request : requête http

    :return paquet http contenant la page"""
    return render('vitrine/rechercheOuvrage.html', locals())


# def ouvrage(request, auteur, titre, num_page):
#     """Affiche les résultats de la recherche d'ouvrage
#
#     :param request : OSEF
#     :param auteur : auteur recherché
#     :param titre : titre recherché
#     :type request : requête http
#     :type auteur : String, peut être ""
#     :type auteur : String, peut être ""
#
#     :return paquet http contenant la page"""
#
#     #Cherche dans la bdd les articles qui contiennent l'auteur et le titre renseigné. Si un des paramètres est vide,
#     #il n'influera pas sur la recherche Si les deux sont vides, on a toute la Bdd
#     n=10
#     query=Ouvrage.objects.filter(Q(auteur__icontains=auteur) & Q(titre__icontains=titre)).order_by("titre")[n*(num_page):n*(num_page+1)]
#     return render(request, 'vitrine/ouvrage.html', {"livres": query, "page": num_page})


def actus(request, tag="", num_page=0):
    """La page actus affiche les n dernières actus du site

    :param request : OSEF
    :param num_page : La page a afficher, définit l'ancienneté des articles qu'on va afficher; les n premiers, puis les n suivants, etc
        (n entier modulable, définit plus loin)
    :param tag : Le tag qu'on recherche éventuellement, peut être ""
    :type request : requête http
    :type num_page : int
    :type tag: String

    :return paquet http contenant la page"""

    #Récupération des n articles avec le tag spécifié
    n = 10
    query = Article.objects.filter(tag__nom_tag__icontains=tag).filter(date__lt=timezone.now()).order_by("-date")[n*(num_page):n*(num_page+1)]
    return render(request, 'vitrine/actus.html', {"last_articles": query, "page" : num_page})
    #/!\ définition valide pour des affichages page par page, mais apparement aussi pour de l'infinite scroll (cf : https://infinite-scroll.com/)


def article(request, id_article=1, num_commentaire=0):
    """page d'un article sépicifique, avec les commentaires en dessous

    page composée de l'article avec l'id_article donné, et des commentaires qui y sont liées, triées par date de publication

    :param request : OSEF
    :param id_article : l'id de l'article à afficher
    :param num_commentaire : La page a afficher, définit l'ancienneté des commentaires qu'on va afficher; les n premiers, puis les n suivants, etc
    :type request : requête HTTP
    :type id_article : int
    :type num_commentaire : int

    :return paquet http contenant la page"""

    article=get_object_or_404(Article, id=id_article)
    n=10
    query = Commentaire.objects.filter(id_article=id_article).order_by("-date")[n*(num_commentaire):n*(num_commentaire+1)]
    return render(request, 'vitrine/article.html', {"article": article, "commentaires": query, "page": num_commentaire})


def festival(request, num_page=0):
    """page sur le festival et le concours BD

        page composée d'une description statique, puis des articles tagués "festival" et "concours"

        :param request : OSEF
        :type request : requête HTTP

        :return paquet http contenant la page"""

    #Récupère les n articles qui ont le tag "festival" ou "concours", met en premier ceux qui sont épinglés, et trie ensuite par date
    n=10
    query = Article.objects.filter(Q(tag="festival") | Q(tag="concours")).filter(date__lt=timezone.now()).order_by("epingler", "-date")[n*(num_page):n*(num_page+1)]
    return render(request, 'vitrine/festival.html', {"last_articles": query, "page": num_page})
    #/!\ définition valide pour des affichages page par page, mais apparement aussi pour de l'infinite scroll (cf : https://infinite-scroll.com/)


def archives(request, tag="", year=timezone.now().year, month=timezone.now().month, num_page=0):
    """La page archive affiche les articles du site triées par tag/date

        :param request : OSEF
        :param tag : Le tag qu'on recherche éventuellement, peut être ""
        :param year : année de recherche des articles
        :param month : mois de recherche des articles
        :param num_page : La page a afficher, définit l'ancienneté des articles qu'on va afficher; les n premiers, puis les n suivants, etc
            (n entier modulable, définit plus loin)
        :type request : requête http
        :type tag: String
        :type num_page : int
        :type year : int
        :type month :int

        :return paquet http contenant la page"""

    # Récupération des n articles avec le tag et la date spécifiés
    n = 10
    query = Article.objects.filter(date__year=year).filter(date__month=month).filter(tag__nom_tag__icontains=tag).filter(date__lt=timezone.now()).order_by("-date")[n * (num_page):n * (num_page + 1)]
    return render(request, 'vitrine/actus.html', {"last_articles": query, "page": num_page})


def infos(request):
    """Page avec les infos sur le club; plan d'accès, coordonnées, réseaux sociaux...

    Page peu destinée à évoluer, donc tout pas de paramètres spécifiques à lui passer, tout est dans le template

    :param request : OSEF
    :type request : requête http

    :return paquet http contenant la page"""
    return render(request, 'vitrine/infos.html', locals())


def contact(request):
    """Page avec un formulaire de contact; un champs remplissable, qui sera envoyé sur une boite mail

    Page peu destinée à évoluer, donc tout pas de paramètres spécifiques à lui passer, tout est dans le template

    :param request : OSEF
    :type request : requête http

    :return paquet http contenant la page"""
    return render(request, 'vitrine/contact.html', locals())
