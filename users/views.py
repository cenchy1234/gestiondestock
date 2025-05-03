from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from users.models import User
from articles.models import Article
from fournisseurs.models import Fournisseur
from stocks.models import StockMovement

# Dashboard view
@login_required
def dashboard(request):
    articles_count = Article.objects.count()
    fournisseurs_count = Fournisseur.objects.count()
    mouvements_count = StockMovement.objects.count()
    return render(request, 'dashboard.html', {
        'articles_count': articles_count,
        'fournisseurs_count': fournisseurs_count,
        'mouvements_count': mouvements_count,
    })

# Login view with role redirection
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == 'admin':
                return redirect('dashboard')
            elif user.role == 'gestionnaire':
                return redirect('article_list')
            else:  # employé
                return redirect('article_list')
        else:
            return render(request, 'login.html', {'error': 'Identifiants invalides'})
    return render(request, 'login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Register view
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        user = User.objects.create_user(username=username, password=password, role=role)
        return redirect('login')
    return render(request, 'register.html')
