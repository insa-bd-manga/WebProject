from django import forms
from captcha.fields import CaptchaField
from .models import Article, Tag

class ContactForm(forms.Form):
    """Formulaire de contact (onglet contact)"""
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse e-mail")
    renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)
    captcha = CaptchaField(label='Si vous êtes un robot, votre chemin s\'arrête ici.')

class CommentForm(forms.Form):
    """Formulaire de commentaire sur les articles"""
    sujet = forms.CharField(max_length=50)
    message = forms.CharField(widget=forms.Textarea) #commentaire de taille infinie
    captcha = CaptchaField(label="prouvez que vous êtes un humain")

class RechercheForm(forms.Form):
    tags_possibles = Tag.objects.all()
    tag = forms.ChoiceField(choices=tags_possibles, label="choix des tags")

    # dates_possibles = Article.date
    # critere = forms.ChoiceField(choices=date_possibles, label="critère de recherche")