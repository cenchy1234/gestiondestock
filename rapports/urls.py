from django.urls import path
from . import views

app_name = 'rapports'

urlpatterns = [
    path('', views.rapport_list, name='rapport_list'),
    path('mouvements/', views.stock_movement_report, name='stock_movement_report'),
    path('etat-stocks/', views.stock_state_report, name='stock_state_report'),
    path('statistiques/', views.statistics_report, name='statistics_report'),

    # API endpoints pour les graphiques
    path('api/stock-evolution/', views.api_stock_evolution, name='api_stock_evolution'),
    path('api/stock-by-category/', views.api_stock_by_category, name='api_stock_by_category'),
    path('api/top-articles/', views.api_top_articles, name='api_top_articles'),
    path('api/monthly-stats/', views.api_monthly_stats, name='api_monthly_stats'),
]
