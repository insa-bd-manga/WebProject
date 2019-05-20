from django.shortcuts import render
from bibliotheque.models import Book, Author, Author_to_book
from bibliotheque.forms import *
from django.db.models import Q

def recherche(request, num_page=0):
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
    serie = ""
    num_page = 0

    #Récupération des n articles avec les critères de recherches inclus en paramètres de la fonction???
    n=20

    #Formulaire de recherche
    form = RechercheLivreForm(request.POST or None)
    if form.is_valid():
        auteur = form.cleaned_data["auteur"]
        genre = form.cleaned_data["genre"]
        titre = form.cleaned_data["titre"]
        serie = form.cleaned_data["serie"]

    #J'ai conscience que le dernier filtre n'est pas intuitif, la conversion de la BDD laisse quelques traces, certains
    #noms ne sont pas forcément pertinents, mais j'ai pas voulu prendre la liberté de les renommer. Ici, ID correspond aux
    #Auteurs d'un ouvrage. Ca fonctionne, par contre, aucun doute là dessus.
    query = Book.objects.filter(title__icontains=titre).filter(kind__icontains=genre).filter(id__name__icontains=auteur).filter(Q(serial_id__title__icontains=serie) | Q(serial_id=None)).order_by("title").distinct()
    nombre_reponses=len(query)
    query = query[n * (num_page):n * (num_page + 1)]

    return render(request, 'bibliotheque/recherche.html', locals())
