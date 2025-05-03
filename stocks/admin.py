from django.contrib import admin
from .models import StockMovement

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('article', 'mouvement_type', 'quantite', 'date_mouvement')
