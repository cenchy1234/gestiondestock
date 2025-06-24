# core/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from stocks.models import StockMovement
from articles.models import Article
import json

@login_required
def dashboard(request):
    # Calculate date range for last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Get movements by date
    daily_movements = StockMovement.objects.filter(
        date_mouvement__range=[start_date, end_date]
    ).annotate(
        date=TruncDate('date_mouvement')
    ).values('date', 'mouvement_type').annotate(
        total=Count('id')
    ).order_by('date')

    # Prepare data for charts
    dates = []
    entrees_data = []
    sorties_data = []
    
    for movement in daily_movements:
        date_str = movement['date'].strftime('%d/%m')
        if date_str not in dates:
            dates.append(date_str)
            
        if movement['mouvement_type'] == 'ENTREE':
            entrees_data.append(movement['total'])
        else:
            sorties_data.append(movement['total'])

    # Get top moved products
    top_products = Article.objects.annotate(
        movement_count=Count('mouvements')
    ).order_by('-movement_count')[:5]

    top_products_labels = [article.nom for article in top_products]
    top_products_data = [article.movement_count for article in top_products]

    # Get articles in critical stock (using stock_disponible and seuil_alerte)
    articles_rupture = []
    for article in Article.objects.all():
        if article.stock_disponible() <= article.seuil_alerte:
            articles_rupture.append(article)

    # Get recent movements
    dernieres_entrees = StockMovement.objects.filter(
        mouvement_type='ENTREE'
    ).order_by('-date_mouvement')[:5]
    
    dernieres_sorties = StockMovement.objects.filter(
        mouvement_type='SORTIE'
    ).order_by('-date_mouvement')[:5]

    # Données pour le graphique en secteurs - répartition par catégorie
    categories_data = []
    categories_labels = []

    for choice in Article.CATEGORIES:
        category_code = choice[0]
        category_name = choice[1]
        count = Article.objects.filter(categorie=category_code).count()
        if count > 0:
            categories_labels.append(category_name)
            categories_data.append(count)

    # Si aucune catégorie, ajouter des données par défaut
    if not categories_data:
        categories_labels = ['Articles']
        categories_data = [Article.objects.count()]

    # Valeur totale du stock
    valeur_stock = sum(article.prix * article.stock_disponible() for article in Article.objects.all())

    context = {
        'total_articles': Article.objects.count(),
        'stock_disponible': sum(article.stock_disponible() for article in Article.objects.all()),
        'total_entrees': StockMovement.objects.filter(mouvement_type='ENTREE').count(),
        'total_sorties': StockMovement.objects.filter(mouvement_type='SORTIE').count(),
        'valeur_stock': valeur_stock,
        'dates_labels': json.dumps(dates),
        'entrees_data': json.dumps(entrees_data),
        'sorties_data': json.dumps(sorties_data),
        'categories_labels': json.dumps(categories_labels),
        'categories_data': json.dumps(categories_data),
        'top_products_labels': json.dumps(top_products_labels),
        'top_products_data': json.dumps(top_products_data),
        'articles_rupture': articles_rupture,
        'dernieres_entrees': dernieres_entrees,
        'dernieres_sorties': dernieres_sorties,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def analytics_dashboard(request):
    """Dashboard Analytics avec IA"""
    return render(request, 'dashboard_analytics.html')
