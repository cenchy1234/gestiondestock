from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StockMovement
from .forms import StockMovementForm
from django.db.models import Sum, F, Q
from django.db.models.functions import Coalesce  # Import Coalesce to handle None values
from core.utils import log_action
from core.decorators import can_view_stock_required, stock_manager_required

@can_view_stock_required
def mouvement_list(request):
    # Fetch all stock movements
    mouvements = StockMovement.objects.all()

    # Calculate stock levels for each article
    stock_levels = (
        StockMovement.objects.values('article__nom', 'article__quantite_initiale')  # Include initial quantity
        .annotate(
            total_entrees=Coalesce(Sum('quantite', filter=Q(mouvement_type='ENTREE')), 0),
            total_sorties=Coalesce(Sum('quantite', filter=Q(mouvement_type='SORTIE')), 0)
        )
        .annotate(stock_disponible=F('article__quantite_initiale') + F('total_entrees') - F('total_sorties'))
    )

    # Ensure no negative stock values
    for stock in stock_levels:
        if stock['stock_disponible'] < 0:
            stock['stock_disponible'] = 0

    # Define a critical stock threshold
    critical_stock_threshold = 10  # Example: 10 units
    critical_stock = [
        stock for stock in stock_levels if stock['stock_disponible'] <= critical_stock_threshold
    ]

    return render(request, 'stocks/mouvement_list.html', {
        'mouvements': mouvements,
        'critical_stock': critical_stock,
    })


@stock_manager_required
def mouvement_create(request):
    from articles.models import Article

    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            mouvement = form.save()
            messages.success(request, f'Mouvement de stock créé: {mouvement.get_mouvement_type_display()} - {mouvement.article.nom} ({mouvement.quantite} unités)')
            log_action(
                request.user,
                f"Création mouvement: {mouvement.mouvement_type} - Article: {mouvement.article.nom} - Quantité: {mouvement.quantite}"
            )
            return redirect('stocks:mouvement_list')
    else:
        form = StockMovementForm()

    # Passer tous les articles pour la vérification JavaScript
    articles = Article.objects.all()
    return render(request, 'stocks/mouvement_form.html', {'form': form, 'articles': articles})


@can_view_stock_required
def check_availability(request, item_id):
    # Get the article associated with the stock movement
    item = get_object_or_404(StockMovement, id=item_id)
    article = item.article

    # Calculate total stock for the article
    total_entrees = StockMovement.objects.filter(
        article=article, mouvement_type='ENTREE'
    ).aggregate(total=Sum('quantite'))['total'] or 0

    total_sorties = StockMovement.objects.filter(
        article=article, mouvement_type='SORTIE'
    ).aggregate(total=Sum('quantite'))['total'] or 0

    stock_disponible = total_entrees - total_sorties

    # Check availability
    is_available = stock_disponible > 0

    return render(request, 'stocks/check_availability.html', {
        'item': item,
        'is_available': is_available,
        'stock_disponible': stock_disponible,
    })
