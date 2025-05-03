# core/views.py

from django.shortcuts import render
from articles.models import Article
from stocks.models import StockMovement

def dashboard_view(request):
    total_articles = Article.objects.count()
    total_stock = sum(article.quantite_initiale for article in Article.objects.all())
    total_entrees = StockMovement.objects.filter(mouvement_type='ENTREE').count()
    total_sorties = StockMovement.objects.filter(mouvement_type='SORTIE').count()

    context = {
        'total_articles': total_articles,
        'total_stock': total_stock,
        'total_entrees': total_entrees,
        'total_sorties': total_sorties,
    }
    return render(request, 'dashboard.html', context)
