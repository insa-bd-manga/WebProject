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

    choix_tags = Tag.objects.all()
    choix_mois = Article.objects.all() #trouver requête qui donne les mois des articles
    choix_annees = Article.objects.all() # Pareil!

    tag = forms.ModelChoiceField(choix_tags, label="choix du tag")
    mois = forms.ModelChoiceField(choix_mois, label="choix du mois")
    annee = forms.ModelChoiceField(choix_annees, label="choix de l'année")


# class TagForm(forms.ModelForm):
#     class Meta:
#         CHOICES = Tag.objects.all()
#
#         model = Tag
#         fields = ('nom_tag',)
#         widgets = {
#             'nom_tag': Select(choices=((x.nom_tag, x.nom_tag) for x in CHOICES)),
#         }
#
#
#
# class ArticleForm(forms.ModelForm):
#     class Meta:
#         CHOICES = Article.objects.all()
#
#         model = Article
#         fields = ('date',)
#         widgets = {
#             'date': Select(choices=((a.date, a.date.year) for a in CHOICES)),
#         }
