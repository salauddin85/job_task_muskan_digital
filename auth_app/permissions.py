from rest_framework.permissions import BasePermission

class NormalUser(BasePermission):
    def has_permission(self, request, view):
        # Normal user can access only if they are not staff or admin
        return request.user and not request.user.is_staff and not request.user.is_admin

class AdminUser(BasePermission):
    def has_permission(self, request, view):
        # Admin user can access if they are staff or admin
        return request.user and (request.user.is_staff or request.user.is_admin)
