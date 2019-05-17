from django import forms
from django.forms.widgets import Select
from captcha.fields import CaptchaField
from .models import Tag, Article

class ContactForm(forms.Form):
    """Formulaire de contact (onglet contact)"""
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse e-mail")
    renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)
    captcha = CaptchaField(label='Si vous êtes un robot, votre chemin s\'arrête ici.')

class CommentForm(forms.Form):
    """Formulaire de commentaire sur les articles"""
    message = forms.CharField(widget=forms.Textarea) #commentaire de taille infinie
    captcha = CaptchaField(label="prouvez que vous êtes un humain")

class RechercheForm(forms.Form):
    # https://docs.djangoproject.com/fr/2.2/ref/models/fields/#field-choices

    #consitution des listes de choix
    choix_tags = Tag.objects.all()

    choix_mois = Article.objects.values_list('date__month', flat=True).order_by('date__month').distinct()
    choix_mois = [(m, m) for m in choix_mois]

    choix_annees = Article.objects.values_list('date__year', flat=True).order_by('date__year').distinct()
    choix_annees = [(a, a) for a in choix_annees]

    #les formulaires
    tag = forms.ModelChoiceField(choix_tags, label="choix du tag", required=False)
    mois = forms.ChoiceField(choices=choix_mois, label="choix du mois", required=False)
    annee = forms.ChoiceField(choices=choix_annees, label="choix de l'année", required=False)
