from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('create/', views.article_create, name='article_create'),
    path('<int:pk>/update/', views.article_update, name='article_update'),
    path('<int:pk>/delete/', views.article_delete, name='article_delete'),
]
