from django.shortcuts import render
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth, TruncDate
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from articles.models import Article
from stocks.models import StockMovement
from .models import Report
import json
import csv
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import io

def rapport_list(request):
    """Vue principale des rapports avec données pour les graphiques"""

    # Données pour les graphiques
    context = {
        'total_articles': Article.objects.count(),
        'total_stock': Article.objects.aggregate(total=Sum('quantite_initiale'))['total'] or 0,
        'mouvements_entrees': StockMovement.objects.filter(mouvement_type='ENTREE').count(),
        'mouvements_sorties': StockMovement.objects.filter(mouvement_type='SORTIE').count(),
    }

    return render(request, 'rapports/rapport_list.html', context)

def stock_movement_report(request):
    movements = StockMovement.objects.annotate(
        month=TruncMonth('date_mouvement')
    ).values('month', 'mouvement_type').annotate(
        total=Sum('quantite')
    ).order_by('month')

    context = {
        'movements': movements,
        'title': 'Rapport des mouvements de stock'
    }

    if request.GET.get('export') == 'pdf':
        return export_pdf(movements, 'mouvements_stock.pdf', 'Mouvements de Stock')
    elif request.GET.get('export') == 'csv':
        return export_csv(movements, 'mouvements_stock.csv')

    return render(request, 'rapports/stock_movement_report.html', context)

def stock_state_report(request):
    # Simplified query that works with any category relation
    stock_by_category = Article.objects.values(
        'categorie'  # Just get the category reference
    ).annotate(
        total_stock=Sum('quantite_initiale'),
        article_count=Count('id')
    ).filter(categorie__isnull=False)

    # Format data using the raw category ID
    formatted_data = []
    for stock in stock_by_category:
        articles = Article.objects.filter(categorie=stock['categorie']).first()
        if articles:
            category_name = str(articles.categorie)  # Use string representation
            formatted_data.append({
                'categorie_nom': category_name,
                'total_stock': stock['total_stock'],
                'article_count': stock['article_count']
            })

    context = {
        'stock_by_category': formatted_data,
        'title': 'État des stocks par catégorie'
    }

    if request.GET.get('export') == 'pdf':
        return export_pdf(formatted_data, 'etat_stocks.pdf', 'État des Stocks')
    elif request.GET.get('export') == 'csv':
        return export_csv(formatted_data, 'etat_stocks.csv')

    return render(request, 'rapports/stock_state_report.html', context)

def statistics_report(request):
    total_entries = StockMovement.objects.filter(
        mouvement_type='ENTREE'
    ).aggregate(total=Sum('quantite'))['total'] or 0

    total_exits = StockMovement.objects.filter(
        mouvement_type='SORTIE'
    ).aggregate(total=Sum('quantite'))['total'] or 0

    monthly_movements = StockMovement.objects.annotate(
        month=TruncMonth('date_mouvement')
    ).values('month').annotate(
        entries=Sum('quantite', filter=Q(mouvement_type='ENTREE')),
        exits=Sum('quantite', filter=Q(mouvement_type='SORTIE'))
    ).order_by('month')

    context = {
        'total_entries': total_entries,
        'total_exits': total_exits,
        'monthly_movements': monthly_movements,
        'title': 'Statistiques des mouvements'
    }

    if request.GET.get('export') == 'pdf':
        return export_pdf(monthly_movements, 'statistiques.pdf', 'Statistiques')
    elif request.GET.get('export') == 'csv':
        return export_csv(monthly_movements, 'statistiques.csv')

    return render(request, 'rapports/statistics_report.html', context)

def export_pdf(data, filename, title):
    """Génération PDF améliorée avec en-tête et mise en forme"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=72, bottomMargin=72)
    elements = []

    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch

    styles = getSampleStyleSheet()

    # Titre du rapport
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=colors.HexColor('#065f46'),
        alignment=1  # Center
    )
    elements.append(Paragraph(title, title_style))

    # Date de génération
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph(f"Généré le {timezone.now().strftime('%d/%m/%Y à %H:%M')}", date_style))
    elements.append(Spacer(1, 20))

    # Convertir les données en format tableau
    if not data:
        table_data = [['Aucune donnée disponible']]
    else:
        # En-têtes traduits
        headers = []
        for key in data[0].keys():
            if key == 'month':
                headers.append('Mois')
            elif key == 'mouvement_type':
                headers.append('Type')
            elif key == 'total':
                headers.append('Total')
            elif key == 'categorie_nom':
                headers.append('Catégorie')
            elif key == 'total_stock':
                headers.append('Stock Total')
            elif key == 'article_count':
                headers.append('Nb Articles')
            else:
                headers.append(str(key).replace('_', ' ').title())

        table_data = [headers]

        for item in data:
            row = []
            for value in item.values():
                if isinstance(value, datetime):
                    row.append(value.strftime('%m/%Y'))
                else:
                    row.append(str(value))
            table_data.append(row)

    # Créer le tableau avec style amélioré
    t = Table(table_data)
    t.setStyle(TableStyle([
        # En-tête
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#065f46')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        # Corps du tableau
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),

        # Alternance de couleurs
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
    ]))

    elements.append(t)

    # Pied de page
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph("Système de Gestion de Stock - Rapport généré automatiquement", footer_style))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def export_csv(data, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    if data:
        writer.writerow(data[0].keys())
        for item in data:
            writer.writerow(item.values())
    else:
        writer.writerow(['Aucune donnée disponible'])

    return response

# API Views pour les graphiques
def api_stock_evolution(request):
    """API pour l'évolution du stock sur les 30 derniers jours"""

    # Calculer les 30 derniers jours
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)

    # Récupérer les mouvements par jour
    daily_movements = StockMovement.objects.filter(
        date_mouvement__date__range=[start_date, end_date]
    ).annotate(
        day=TruncDate('date_mouvement')
    ).values('day', 'mouvement_type').annotate(
        total=Sum('quantite')
    ).order_by('day')

    # Organiser les données
    dates = []
    entrees = []
    sorties = []

    # Créer un dictionnaire pour faciliter l'organisation
    data_dict = {}
    for movement in daily_movements:
        day_str = movement['day'].strftime('%Y-%m-%d')
        if day_str not in data_dict:
            data_dict[day_str] = {'entrees': 0, 'sorties': 0}

        if movement['mouvement_type'] == 'ENTREE':
            data_dict[day_str]['entrees'] = movement['total']
        else:
            data_dict[day_str]['sorties'] = movement['total']

    # Remplir les listes pour les 30 derniers jours
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        dates.append(current_date.strftime('%d/%m'))

        if date_str in data_dict:
            entrees.append(data_dict[date_str]['entrees'])
            sorties.append(data_dict[date_str]['sorties'])
        else:
            entrees.append(0)
            sorties.append(0)

        current_date += timedelta(days=1)

    return JsonResponse({
        'dates': dates,
        'entrees': entrees,
        'sorties': sorties
    })

def api_stock_by_category(request):
    """API pour la répartition du stock par catégorie"""

    # Récupérer les articles avec leur stock par catégorie
    categories_data = Article.objects.values('categorie').annotate(
        total_stock=Sum('quantite_initiale'),
        count=Count('id')
    ).filter(categorie__isnull=False, total_stock__gt=0)

    labels = []
    data = []
    colors = ['#065f46', '#059669', '#10b981', '#34d399', '#6ee7b7', '#a7f3d0']

    for i, category in enumerate(categories_data):
        # Obtenir le nom de la catégorie
        try:
            article = Article.objects.filter(categorie=category['categorie']).first()
            if article:
                category_name = str(article.categorie)
                labels.append(category_name)
                data.append(category['total_stock'])
        except:
            labels.append(f"Catégorie {category['categorie']}")
            data.append(category['total_stock'])

    return JsonResponse({
        'labels': labels,
        'data': data,
        'colors': colors[:len(labels)]
    })

def api_top_articles(request):
    """API pour les articles les plus mouvementés"""

    # Récupérer les articles avec le plus de mouvements
    top_articles = StockMovement.objects.values(
        'article__nom', 'article__reference'
    ).annotate(
        total_mouvements=Count('id'),
        total_quantite=Sum('quantite')
    ).order_by('-total_mouvements')[:10]

    labels = []
    mouvements = []
    quantites = []

    for article in top_articles:
        labels.append(article['article__nom'][:20])  # Limiter la longueur
        mouvements.append(article['total_mouvements'])
        quantites.append(article['total_quantite'])

    return JsonResponse({
        'labels': labels,
        'mouvements': mouvements,
        'quantites': quantites
    })

def api_monthly_stats(request):
    """API pour les statistiques mensuelles"""

    # Récupérer les 12 derniers mois
    end_date = timezone.now().date()
    start_date = end_date.replace(day=1) - timedelta(days=365)

    monthly_data = StockMovement.objects.filter(
        date_mouvement__date__gte=start_date
    ).annotate(
        month=TruncMonth('date_mouvement')
    ).values('month', 'mouvement_type').annotate(
        total=Sum('quantite')
    ).order_by('month')

    # Organiser les données par mois
    months = []
    entrees = []
    sorties = []

    data_dict = {}
    for movement in monthly_data:
        month_str = movement['month'].strftime('%Y-%m')
        if month_str not in data_dict:
            data_dict[month_str] = {'entrees': 0, 'sorties': 0}

        if movement['mouvement_type'] == 'ENTREE':
            data_dict[month_str]['entrees'] = movement['total']
        else:
            data_dict[month_str]['sorties'] = movement['total']

    # Générer les 12 derniers mois
    current_date = start_date
    while current_date <= end_date:
        month_str = current_date.strftime('%Y-%m')
        months.append(current_date.strftime('%b %Y'))

        if month_str in data_dict:
            entrees.append(data_dict[month_str]['entrees'])
            sorties.append(data_dict[month_str]['sorties'])
        else:
            entrees.append(0)
            sorties.append(0)

        # Passer au mois suivant
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)

    return JsonResponse({
        'months': months,
        'entrees': entrees,
        'sorties': sorties
    })
