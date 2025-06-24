from django.urls import path
from . import views

app_name = 'fournisseurs'

urlpatterns = [
    # Fournisseur URLs
    path('', views.fournisseur_list, name='fournisseur_list'),
    path('create/', views.fournisseur_create, name='fournisseur_create'),
    path('<int:pk>/', views.fournisseur_detail, name='fournisseur_detail'),
    path('<int:pk>/update/', views.fournisseur_update, name='fournisseur_update'),
    path('<int:pk>/delete/', views.fournisseur_delete, name='fournisseur_delete'),
    
    # Commande URLs
    path('commandes/', views.commande_list, name='commande_list'),
    path('commandes/create/', views.commande_create, name='commande_create'),
    path('commandes/<int:pk>/update-status/', views.commande_update_status, name='commande_update_status'),
]
