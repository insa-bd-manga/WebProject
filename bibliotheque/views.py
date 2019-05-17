from django.shortcuts import render
from bibliotheque.models import Book, Author, Author_to_book
from .forms import *

def recherche(request):
    """page de "moteur de recherche d'ouvrages"

        page avec un formulaire permettant de rechercher les livres par genre/titre/auteur

        :param request : OSEF
        :param auteur : l'auteur recherché
        :param genre : le genre recherché
        :param titre : Le titre recherché
        :param num_page : La page a afficher

        :type request : requête HTTP
        :type auteur : String
        :type genre : String
        :type titre : String
        :type num_page : int

        :return paquet http contenant la page"""

    #Déclaration initiale des variables
    auteur = ""
    genre = ""
    titre = ""
    num_page = 0

    #Récupération des n articles avec les critères de recherches inclus en paramètres de la fonction???
    n=10

    #J'ai conscience que le dernier filtre n'est pas intuitif, la conversion de la BDD laisse quelques traces, certains
    #noms ne sont pas forcément pertinents, mais j'ai pas voulu prendre la liberté de les renommer. Ici, ID correspond aux
    #Auteurs d'un ouvrage. Ca fonctionne, par contre, aucun doute là dessus.
    query = Book.objects.filter(title__icontains=titre).filter(kind__icontains=genre).filter(id__name__icontains=auteur).order_by("title")
    nombre_reponses=len(query)
    query = query[n * (num_page):n * (num_page + 1)]

    #Formulaire de recherche
    form = RechercheLivreForm(request.POST or None)
    if form.is_valid():
        auteur = form.cleaned_data["auteur"]
        genre = form.cleaned_data["genre"]
        titre = form.cleaned_data["titre"]

    return render(request, 'bibliotheque/recherche.html', locals())
