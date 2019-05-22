from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect

#pour les modèles
from vitrine.models import Article, Commentaire, Tag

#Pour des query plus complexes que le set de base
from django.db.models import Q

#Pour les mails
from django.core.mail import send_mail

#Pour la data
from django.utils import timezone

#pour les formulaires
from .forms import ContactForm, CommentForm, RechercheForm

from math import *

def index(request):
    """l'index est la page d'accueil du site

    page composée d'une description statique, puis des 3 derniers articles sortis

    :param request : OSEF
    :type request : requête HTTP

    :return paquet http contenant la page"""

    # récupération des 3 derniers articles en date
    query = Article.objects.all().filter(date__lt=timezone.now()).order_by("-date")[:3]

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
    query = Article.objects.filter(tag__nom_tag__icontains=tag).filter(date__lt=timezone.now()).order_by("-date")
    nbr_articles = len(query)
    pages_necessaires = ceil((nbr_articles/10))-1 #nombre de pages necessaire pour afficher tout les articles -1 du à l'indexation commencant à 0

    query = query[n * (num_page):n * (num_page + 1)]
    return render(request, 'vitrine/actus.html', {"last_articles": query, "page" : num_page, "tag": tag, "nbr_articles":nbr_articles,"pages_necess":pages_necessaires})
    #/!\ définition valide pour des affichages page par page, mais apparement aussi pour de l'infinite scroll (cf : https://infinite-scroll.com/)


def article(request, id_article=1, page_commentaire=0):
    """page d'un article sépicifique, avec les commentaires en dessous

    page composée de l'article avec l'id_article donné, et des commentaires qui y sont liées, triées par date de publication

    :param request : OSEF
    :param id_article : l'id de l'article à afficher
    :param page_commentaire : La page a afficher, définit l'ancienneté des commentaires qu'on va afficher; les n premiers, puis les n suivants, etc
    :type request : requête HTTP
    :type id_article : int
    :type page_commentaire : int

    :return paquet http contenant la page"""

    # acquisition de l'article
    article = get_object_or_404(Article, id=id_article)
    # acquisition des 50 derniers commentaires
    n = 10
    commentaires = Commentaire.objects.filter(id_article=id_article).order_by("date")
    nbr_comms = len(commentaires)
    pages_comms_necessaires = ceil((nbr_comms / 10)) - 1
    commentaires = commentaires[n*(page_commentaire):n*(page_commentaire+1)]


    # formulaire de commentaire
    envoi = False

    form = CommentForm(request.POST or None)
    if form.is_valid():
        new_com = Commentaire()
        new_com.id_article = article
        new_com.contenu = form.cleaned_data['message']
        new_com.save()

        # si envoie réussi
        envoi = True

    return render(request, 'vitrine/article.html', locals())


def festival(request, num_page=0):
    """page sur le festival et le concours BD

        page composée d'une description statique, puis des articles tagués "festival" et "concours"

        :param request : OSEF
        :type request : requête HTTP

        :return paquet http contenant la page"""

    #Récupère les n articles qui ont le tag "festival" ou "concours", met en premier ceux qui sont épinglés, et trie ensuite par date
    n = 10
    query = Article.objects.filter(Q(tag__nom_tag__icontains="festival") | Q(tag__nom_tag__icontains="concours")).filter(date__lt=timezone.now()).order_by("-epingler", "-date")
    nbr_articles = len(query)
    pages_necess = ceil((nbr_articles/10))-1 #nombre de pages necessaire pour afficher tout les articles -1 du à l'indexation commencant à 0
    query = query[n*(num_page):n*(num_page+1)]
    return render(request, 'vitrine/festival.html', {"last_articles": query, "page": num_page, "pages_necessaires": pages_necess })
    #/!\ définition valide pour des affichages page par page, mais apparement aussi pour de l'infinite scroll (cf : https://infinite-scroll.com/)


tag_URL = ""
year_URL = ""
month_URL = ""

def archives(request, num_page=0):
    """La page archive affiche les articles du site selon la demande de l'utilisateur.

    L'utilisateur peut choisir de retrouver des articles selon le mois, l'année ou le(s) tag(s). Ce choix se fait via 3
    menus déroulants.
    Cette view utilise le fomulaire "RecherchForm"
    Les variables dispos pour le template sont :
        -tag, annee, mois les paramètres de recherche de l'utilisateur (string vide si non renseigné)
        -form le formulaire avec les 3 menus déroulants

        :param request : OSEF
        :param num_page : La page a afficher, définit l'ancienneté des articles qu'on va afficher; les n premiers, puis les n suivants, etc
            (n entier modulable, définit plus loin)
        :type request : requête http
        :type num_page : int

        :return paquet http contenant la page SI requete GET
        :return redirection vers la page d'archive souhaitée SI requete POST"""

    global tag_URL
    global year_URL
    global month_URL

    # Récupération des paramètres depuis l'URL, avec paramètres par DEFAUT
    if(request.method == 'GET'):
        tag_URL = request.GET.get('tag', default="")
        year_URL = request.GET.get('year')
        month_URL = request.GET.get('month')

        # Si les champs année et mois ne sont pas renseignés : date actuelle
        if year_URL is None:
            year_URL = ""
        if month_URL is None:
            month_URL = ""

    n = 100 #nombre d'articles par page

    # Récupération des n articles avec le tag et la date spécifiés
    query = Article.objects.filter(date__year__icontains=year_URL).filter(date__month__icontains=month_URL)\
                .filter(tag__nom_tag__icontains=tag_URL).filter(date__lt=timezone.now())\
                .order_by("-date")[n * (num_page):n * (num_page + 1)]

    #récupération des infos du formulaire
    form = RechercheForm(request.POST or None)
    if form.is_valid():
        requete_tag = form.cleaned_data.get('tag')
        requete_mois = form.cleaned_data.get('mois')
        requete_annee = form.cleaned_data.get('annee')

        if requete_tag==None:
            requete_tag = tag_URL

        if requete_mois is None or requete_mois == "":
            requete_mois = month_URL

        if requete_annee is None or requete_annee == "":
            requete_annee = year_URL
        return redirect("/archives/{}?tag={}&year={}&month={}".format(num_page, requete_tag, requete_annee, requete_mois))

    else:
        variables_template = dict(locals(),**{"tag":tag_URL, "annee":year_URL, "mois":month_URL})
        return render(request, 'vitrine/archives.html', variables_template)


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

    :return paquet http contenant la page

    :raise SMTPException : si l'envoi du mail foire."""

    envoi = False

    form = ContactForm(request.POST or None)
    if form.is_valid():
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']
        envoyeur = form.cleaned_data['envoyeur']
        renvoi = form.cleaned_data['renvoi']

        #envoie mail pour le club
        sujet_mail = "[contact site] {}".format(sujet)
        contenu_mail = '\n'.join(["message de la part de : {}".format(envoyeur), "", message])
        send_mail(sujet_mail, contenu_mail, "clubbdinsa@outlook.fr", ['clubbdinsa@gmail.com'], fail_silently=False)

        #envoie mail facultatif pour le client
        if renvoi == True:
            sujet_mail = "[copie contact INSA BD/Manga] {}".format(sujet)
            send_mail(sujet_mail, contenu_mail, "clubbdinsa@outlook.fr", [envoyeur], fail_silently=False)

        #si envoie réussi
        envoi = True

    return render(request, 'vitrine/contact.html', {"envoi": envoi, "form":form})
