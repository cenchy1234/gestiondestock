from django import forms
from .models import StockMovement

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['article', 'mouvement_type', 'quantite']
