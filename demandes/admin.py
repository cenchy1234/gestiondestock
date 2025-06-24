from django.contrib import admin
from .models import Demande, HistoriqueDemande

@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ['numero_demande', 'demandeur', 'article', 'quantite_demandee', 'statut', 'priorite', 'date_demande']
    list_filter = ['statut', 'priorite', 'date_demande']
    search_fields = ['numero_demande', 'demandeur__username', 'article__nom']
    readonly_fields = ['numero_demande', 'date_demande']

@admin.register(HistoriqueDemande)
class HistoriqueDemandeAdmin(admin.ModelAdmin):
    list_display = ['demande', 'utilisateur', 'action', 'date_action']
    list_filter = ['action', 'date_action']
    search_fields = ['demande__numero_demande', 'utilisateur__username']
