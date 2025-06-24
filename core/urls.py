from django.urls import path
from . import views, api_views
from django.contrib.auth import views as auth_views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # API endpoints pour les fonctionnalités IA et temps réel
    path('api/live-stats/', api_views.live_stats_api, name='live_stats_api'),
    path('api/ai-predictions/', api_views.ai_predictions_api, name='ai_predictions_api'),
    path('api/recommendations/', api_views.smart_recommendations_api, name='recommendations_api'),
    path('api/performance/', api_views.performance_metrics_api, name='performance_api'),
    path('api/alerts/', api_views.alerts_api, name='alerts_api'),
    path('api/webhook/notifications/', api_views.NotificationWebhook.as_view(), name='notification_webhook'),
]
