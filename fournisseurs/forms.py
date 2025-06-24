from django import forms
from .models import Fournisseur, Commande

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'adresse', 'telephone', 'email']

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['fournisseur', 'article', 'quantite']
        widgets = {
            'fournisseur': forms.Select(attrs={'class': 'form-control'}),
            'article': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
        }
