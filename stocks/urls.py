from django.urls import path
from . import views

urlpatterns = [
    path('', views.mouvement_list, name='mouvement_list'),
    path('create/', views.mouvement_create, name='mouvement_create'),
]
