from django.urls import path
from . import views

app_name = 'demandes'

urlpatterns = [
    # Liste et gestion des demandes
    path('', views.demande_list, name='demande_list'),
    path('mes-demandes/', views.mes_demandes, name='mes_demandes'),
    path('nouvelle/', views.demande_create, name='demande_create'),
    path('<int:pk>/', views.demande_detail, name='demande_detail'),
    path('<int:pk>/traiter/', views.demande_traiter, name='demande_traiter'),
    path('<int:pk>/livrer/', views.demande_livrer, name='demande_livrer'),
    
    # AJAX
    path('check-stock/', views.check_stock_ajax, name='check_stock_ajax'),
]
