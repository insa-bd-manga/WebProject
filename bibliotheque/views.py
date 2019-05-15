from django.shortcuts import render
from bibliotheque.models import Book, Author, Author_to_book

def recherche(request):
    """page de "moteur de recherche d'ouvrages"

        page avec un formulaire permettant de rechercher les livres par genre/titre/auteur

        :param request : OSEF
        :type request : requête HTTP

        :return paquet http contenant la page"""

    return render(request, 'bibliotheque/recherche.html', locals())

def resultats(request):
    """Affiche les résultats de la recherche précédente

    :param request : OSEF
    :param auteur : l'auteur recherché
    :param genre : le genre recherché
    :param titre : Le titre recherché
    :param num_page : La page a afficher

    :type request : requete http
    :type auteur : String
    :type genre : String
    :type titre : String
    :type num_page : int

    :return paquet http contenant la page"""

    auteur = request.GET(['auteur'])
    genre = request.GET(['genre'])
    titre = request.GET(['titre'])
    num_page = request.GET['num_page']

    #Récupération des n articles avec les critères de recherches inclus en paramètres de la fonction???
    n=10

    #J'ai conscience que le dernier filtre n'est pas intuitif, la conversion de la BDD laisse quelques traces, certains
    #noms ne sont pas forcément pertinents, mais j'ai pas voulu prendre la liberté de les renommer. Ici, ID correspond aux
    #Auteurs d'un ouvrage.
    query = Book.objects.filter(title__icontains=titre).filter(kind__icontains=genre).filter(id__name__icontains=auteur).order_by("title")
    nombre_reponses=len(query)
    query = query[n * (num_page):n * (num_page + 1)]
    return render(request, 'bibliotheque/resultats.html', {"livres": query, "page": num_page, "nombre_reponses": nombre_reponses})

