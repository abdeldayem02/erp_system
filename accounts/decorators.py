from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponseForbidden

def admin_required(view_func):
    """
    Decorator for views that checks that the user is logged in and has admin role.
    Redirects to login page if not authenticated, or returns 403 if not admin.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin():
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


def sales_required(view_func):
    """
    Decorator for views that checks that the user is logged in and has sales role.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_sales():
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper
