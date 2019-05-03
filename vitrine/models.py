from django.db import models
from django.utils import timezone


class Tag(models.Model):
    nom_tag = models.CharField(max_length=30)

    def __str__(self):
        return self.nom_tag


class Article(models.Model):
    titre = models.CharField(max_length=100)
    auteur = models.CharField(max_length=42)
    contenu = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Date de parution")
    categorie = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.titre


