from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('users:login'), name='home'),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('articles/', include('articles.urls', namespace='articles')),
    path('stocks/', include('stocks.urls', namespace='stocks')),
    path('rapports/', include('rapports.urls')),
    path('fournisseurs/', include('fournisseurs.urls', namespace='fournisseurs')),
    path('demandes/', include('demandes.urls', namespace='demandes')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

