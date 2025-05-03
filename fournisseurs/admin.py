from django.contrib import admin
from .models import Fournisseur, Commande

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone')

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('fournisseur', 'article', 'quantite', 'date_commande', 'statut')
