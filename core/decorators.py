from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    """Décorateur pour les vues accessibles uniquement aux administrateurs"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, "Accès refusé. Seuls les administrateurs peuvent accéder à cette page.")
            return redirect('core:dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def stock_manager_required(view_func):
    """Décorateur pour les vues accessibles aux gestionnaires de stock et administrateurs"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.can_manage_stock():
            messages.error(request, "Accès refusé. Vous n'avez pas les permissions pour gérer les stocks.")
            return redirect('core:dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def can_view_stock_required(view_func):
    """Décorateur pour les vues de consultation des stocks (tous les rôles)"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.can_view_stock():
            messages.error(request, "Accès refusé. Vous n'avez pas les permissions pour consulter les stocks.")
            return redirect('core:dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def employee_or_higher_required(view_func):
    """Décorateur pour les vues accessibles aux employés et plus"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.can_view_stock():
            messages.error(request, "Accès refusé.")
            return redirect('core:dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
