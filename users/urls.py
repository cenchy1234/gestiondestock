from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.user_create, name='user_create'),
    path('', views.user_list, name='user_list'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('<int:user_id>/update/', views.user_update, name='user_update'),
    path('<int:user_id>/delete/', views.user_delete, name='user_delete'),
]
