from django.shortcuts import render
from .models import Fournisseur

def fournisseur_list(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseurs/fournisseur_list.html', {'fournisseurs': fournisseurs})
