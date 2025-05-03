from django.urls import path
from . import views

urlpatterns = [
    path('', views.rapport_list, name='rapport_list'),
]
