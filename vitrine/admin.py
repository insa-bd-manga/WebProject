from django.contrib import admin
from django.utils.text import Truncator
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from vitrine.models import Tag, Article, Commentaire


class ArticleAdminForm(forms.ModelForm):
    """Cette class définit le champs pour la rédaction d'articles.

    Utilise le widget CKEditor pour faire des beaux articles en HTML
    #TODO : si on a le temps, ajouter l'upload de fichier.
    En effet, actuellement, on ne peut ajouter des images que depuis une URL."""

    contenu = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
    """Cette class définit l'espace d'édition des articles.

    Utilise la classe ArticleAdminForm"""

    list_display = ('titre', 'auteur', 'get_tag', 'apercu_contenu', 'date')
    list_filter = ('titre', 'auteur', 'tag', 'date')
    #ordering = ('date',)
    search_fields = ('titre', 'contenu')

    # Configuration du formulaire d'édition
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
        ('Général', {
            'fields': ('titre', 'auteur', 'date', 'tag')
        }),
        # Fieldset 2 : contenu de l'article
        ('Contenu de l\'article', {
            'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
            'fields': ('contenu',)
        }),
    )

    form = ArticleAdminForm


    def apercu_contenu(self, article):
        """Retourne les 40 premiers caractères du contenu de l'article,
        suivi de points de suspension si le texte est plus long.
        """
        return Truncator(article.contenu).chars(40, truncate='...')

    # En-tête de notre colonne
    apercu_contenu.short_description = 'Aperçu du contenu'



admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Commentaire)
