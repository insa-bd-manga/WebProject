from django.contrib import admin
from django.utils.text import Truncator
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Tag, Article, Commentaire


class ArticleAdminForm(forms.ModelForm):
    contenu = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
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
        """
        Retourne les 40 premiers caractères du contenu de l'article,
        suivi de points de suspension si le texte est plus long.
        """
        return Truncator(article.contenu).chars(40, truncate='...')

    # En-tête de notre colonne
    apercu_contenu.short_description = 'Aperçu du contenu'

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Commentaire)

#admin.site.site_header(path('/admin/documentation', views.doc, name='doc'))
# class MyModelAdmin(admin.ModelAdmin):
#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('documentation/', self.documentation),
#         ]
#         return my_urls + urls
#
#     def documentation(self, request):
#
#         return TemplateResponse(request, "documentation.html")

