from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('mouvements/', views.mouvement_list, name='mouvement_list'),
    path('mouvements/create/', views.mouvement_create, name='mouvement_create'),
    path('mouvements/check/<int:item_id>/', views.check_availability, name='check_availability'),
]
