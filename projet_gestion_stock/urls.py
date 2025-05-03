from django.contrib import admin
from django.urls import path, include
from core.views import dashboard_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('articles/', include('articles.urls')),
    path('stocks/', include('stocks.urls')),
    path('fournisseurs/', include('fournisseurs.urls')),
    path('rapports/', include('rapports.urls')),
     path('dashboard/', dashboard_view, name='dashboard'),
     
]

