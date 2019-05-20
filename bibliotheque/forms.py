from django import forms
from bibliotheque.models import *


class RechercheLivreForm(forms.Form):
    choix_genre = (('b', "BD"), ('m', "Manga"))

    genre = forms.ChoiceField(choices=choix_genre, label="Genre", required=False)
    auteur = forms.CharField(max_length=40, required=False)
    titre = forms.CharField(max_length=100, required=False)
    serie = forms.CharField(max_length=100, required=False)
