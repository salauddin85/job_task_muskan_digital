from rest_framework.permissions import BasePermission

class IsAdminOrOwnModule(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Admin users can do everything
            if request.user.is_admin:
                return True
            # Non-admin users can only access their own modules
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Admins can access all objects
        if request.user.is_admin:
            return True
        # Non-admin users can only view their own modules
        return obj.user == request.user
