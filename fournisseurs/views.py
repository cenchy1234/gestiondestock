from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Fournisseur, Commande
from .forms import FournisseurForm, CommandeForm
from core.utils import log_action
from core.decorators import stock_manager_required

@stock_manager_required
def fournisseur_list(request):
    fournisseurs = Fournisseur.objects.all()
    print(fournisseurs)  # Debug: Print the fournisseurs queryset
    return render(request, 'fournisseurs/fournisseur_list.html', {'fournisseurs': fournisseurs})

@stock_manager_required
def fournisseur_create(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            fournisseur = form.save()
            messages.success(request, f'Fournisseur "{fournisseur.nom}" créé avec succès!')
            return redirect('fournisseurs:fournisseur_list')
    else:
        form = FournisseurForm()
    return render(request, 'fournisseurs/fournisseur_form.html', {'form': form})

@stock_manager_required
def fournisseur_detail(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    return render(request, 'fournisseurs/fournisseur_detail.html', {'fournisseur': fournisseur})

@stock_manager_required
def fournisseur_update(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            messages.success(request, f'Fournisseur "{fournisseur.nom}" modifié avec succès!')
            return redirect('fournisseurs:fournisseur_list')
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'fournisseurs/fournisseur_form.html', {'form': form})

@stock_manager_required
def fournisseur_delete(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        nom = fournisseur.nom
        fournisseur.delete()
        messages.success(request, f'Fournisseur "{nom}" supprimé avec succès!')
        return redirect('fournisseurs:fournisseur_list')
    return render(request, 'fournisseurs/fournisseur_confirm_delete.html', {'fournisseur': fournisseur})

@stock_manager_required
def commande_list(request):
    commandes = Commande.objects.all()
    return render(request, 'fournisseurs/commande_list.html', {'commandes': commandes})

@stock_manager_required
def commande_create(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save()
            log_action(
                request.user,
                f"Création commande: Fournisseur: {commande.fournisseur.nom} - Article: {commande.article.nom}"
            )
            return redirect('fournisseurs:commande_list')
    else:
        form = CommandeForm()
    return render(request, 'fournisseurs/commande_form.html', {'form': form})

@login_required
def commande_update_status(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        statut = request.POST.get('statut')
        if statut:
            old_status = commande.get_statut_display()
            commande.statut = statut
            commande.save()
            log_action(
                request.user,
                f"Mise à jour statut commande #{commande.id}: {old_status} -> {commande.get_statut_display()}"
            )
            return redirect('fournisseurs:commande_list')
    return render(request, 'fournisseurs/commande_update_status.html', {'commande': commande})