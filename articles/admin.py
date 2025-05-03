from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'reference', 'categorie', 'prix', 'quantite_initiale', 'date_ajout')
