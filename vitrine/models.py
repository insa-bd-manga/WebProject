from django.db import models
from django.utils import timezone


class Tag(models.Model):
    """Tag pour les articles
    :clé_primaire id: généré implicitement"""
    nom_tag = models.CharField(max_length=30)

    def __str__(self):
        return self.nom_tag


class Article(models.Model):
    """Article
    :clé_primaire id: généré implicitement
    :clé_étrangère tag: ManyToMany (un article peut avoir 0,1,plusieurs tags et vice-versa)"""
    titre = models.CharField(max_length=100)
    auteur = models.CharField(max_length=50, null=True, verbose_name="auteur de l'article")
    date = models.DateTimeField(default=timezone.now, verbose_name="date de parution")
    contenu = models.TextField()
    tag = models.ManyToManyField(Tag)
    epingler = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.titre

    def get_tag(self):
        """retourne les tags dans un string sous la forme "tag1, tag2, tag3" """
        return ", ".join([a.nom_tag for a in self.tag.all()])


class Commentaire(models.Model):
    """Commentaire lié à un article
    :clé_primaire id: généré implicitement
    :clé_étrangère id_article: OneToMany (un commentaire ne peut être lié qu'à un seul article et un article peut avoir
    plusieurs commentaires)"""
    id_article = models.ForeignKey('Article', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    #auteur = models.ForeignKey('Auteur', null=True, on_delete=models.SET_NULL)
    contenu = models.TextField()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.contenu

