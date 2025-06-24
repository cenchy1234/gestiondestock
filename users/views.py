from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from articles.models import Article
from stocks.models import StockMovement
from .forms import CustomAuthenticationForm, AdminUserCreationForm, UserUpdateForm
from .models import User
from core.decorators import admin_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} ({user.get_role_display()})!')
            next_url = request.GET.get('next', 'core:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return render(request, 'login.html', {'error': 'Identifiants invalides'})
    return render(request, 'login.html')

@admin_required
def user_create(request):
    """Seuls les administrateurs peuvent créer des comptes"""
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Compte créé avec succès pour {user.username} avec le rôle {user.get_role_display()}!')
            return redirect('users:user_list')
    else:
        form = AdminUserCreationForm()

    return render(request, 'users/user_create.html', {'form': form})

@admin_required
def user_list(request):
    """Liste des utilisateurs - accessible uniquement aux administrateurs"""
    users = User.objects.all().order_by('username')
    paginator = Paginator(users, 10)  # 10 utilisateurs par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/user_list.html', {'page_obj': page_obj})

@admin_required
def user_detail(request, user_id):
    """Détails d'un utilisateur - accessible uniquement aux administrateurs"""
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/user_detail.html', {'user_detail': user})

@admin_required
def user_update(request, user_id):
    """Modification d'un utilisateur - accessible uniquement aux administrateurs"""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save()
            # Gérer le champ is_active séparément
            updated_user.is_active = 'is_active' in request.POST
            updated_user.save()
            messages.success(request, f'Utilisateur {updated_user.username} mis à jour avec succès!')
            return redirect('users:user_detail', user_id=updated_user.id)
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'users/user_update.html', {'form': form, 'user_detail': user})

@admin_required
def user_delete(request, user_id):
    """Suppression d'un utilisateur - accessible uniquement aux administrateurs"""
    user = get_object_or_404(User, id=user_id)
    if request.user == user:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect('users:user_list')

    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Utilisateur {username} supprimé avec succès!')
        return redirect('users:user_list')
    return render(request, 'users/user_confirm_delete.html', {'user_detail': user})

def logout_view(request):
    logout(request)
    return redirect('users:login')

@login_required
def dashboard(request):
    context = {
        'total_articles': Article.objects.count(),
        'stock_disponible': sum(article.quantite_initiale for article in Article.objects.all()),
        'total_entrees': StockMovement.objects.filter(mouvement_type='ENTREE').count(),
        'total_sorties': StockMovement.objects.filter(mouvement_type='SORTIE').count(),
    }
    return render(request, 'dashboard.html', context)
