from django.db import models
from django.utils import timezone


"""
A toi qui entretient ce code, il diffère un peur du reste du site, et tu peux être un peu surpris.
Tout d'abord, si il est en anglais, contrairement au reste du code, c'est parceque la base de donnée qu'on utilise n'est 
pas créée par nous, on la récupère, et elle existait déjà. Pour s'y retrouver, on a donc mis les noms de variables de
l'ancienne BDD.

Tu constateras aussi qu'il y a des options inutiles; les null = False par exemple. Ceci afin de pouvoir voir d'un seul
coup d'oeil si notre structure correspond correctement à celle qu'il y avait avant. 

On force également une ID en clef primaire, alors que DJango le gère plus ou moins tout seul, pour retrouver aussi les 
données de l'ancienne base, et limiter les problèmes de compatibilité. 

Sinon, rien de bien compliqué ici, si tu as des doutes je t'invite à aller voir par ici:
https://openclassrooms.com/fr/courses/1871271-developpez-votre-site-web-avec-le-framework-django/1872229-les-modeles
"""

class History(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    book_id = models.IntegerField(null=False)
    user_id = models.IntegerField(null=False)
    date_start = models.DateTimeField(default=timezone.now, null=False)
    date_end = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        ordering = ['date_start']


class Editor(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=40, unique=True, null=False)


class Author(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=40, unique=True, null=False)


class Serial(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    title = models.CharField(max_length=100, unique=True, null=True)


class User(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    lastname = models.CharField(max_length=40, null=False)
    firstname = models.CharField(max_length=40, null=False)
    student_number = models.CharField(max_length=10, null=True)
    mail = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=255, null=True)
    nb_items = models.IntegerField(default=0, null=False)
    year = models.IntegerField(null=False)

    class Meta:
        ordering = ['year', 'lastname', 'firstname']


class Book(models.Model):
    #On passe par la classe ci-dessus et non pas par la définition de base de DJango, pour avoir l'unicité des couples.
    id = models.ManyToManyField(Author, through='Author_to_book', related_name="auteur")
    title = models.CharField(max_length=100, null=False)
    serial_id = models.ForeignKey(Serial, on_delete=models.PROTECT, null=True) #Apparait dans SQLite comme serial_id_id
    serial_nb = models.IntegerField(null=True)
    ean = models.CharField(max_length=13, null=True)
    editor = models.ForeignKey(Editor, on_delete=models.PROTECT, null=True) #Même chose, editor_id
    buy_date = models.DateTimeField(default=timezone.now, null=True)
    reference = models.CharField(max_length=10, unique=True, null=False)
    kind = models.CharField(max_length=1, null=False)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True) #Même chose
    date_start = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        ordering = ['kind', 'title']


class Author_to_book(models.Model):
    author_id = models.ForeignKey(Author, on_delete=models.PROTECT, null=False)
    book_id = models.ForeignKey(Book, on_delete=models.PROTECT, null=False)

    class Meta:
        #Couples auteur/livres uniques grâce à ceci:
        unique_together = (("author_id", "book_id"),)
