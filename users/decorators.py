from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.can_manage_users():
            return redirect('403')
        return view_func(request, *args, **kwargs)
    return wrapper

def stock_manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.can_manage_stock():
            return redirect('403')
        return view_func(request, *args, **kwargs)
    return wrapper

def employee_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.can_view_stock():
            return redirect('403')
        return view_func(request, *args, **kwargs)
    return wrapper
