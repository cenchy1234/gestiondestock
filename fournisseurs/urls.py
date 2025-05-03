from django.urls import path
from . import views

urlpatterns = [
    path('', views.fournisseur_list, name='fournisseur_list'),
]
