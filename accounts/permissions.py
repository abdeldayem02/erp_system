from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin())
    

class IsSalesUser(BasePermission):
    """
    Allows access only to sales users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_sales())
    

class AdminOrReadOnly(BasePermission):
    """
    The request is authenticated as an admin user, or is a read-only for sales user.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_admin():
            return True
        return request.method in ('GET', 'HEAD', 'OPTIONS')