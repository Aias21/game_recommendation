from rest_framework.permissions import BasePermission


CUSTOM_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in CUSTOM_METHODS and request.user.is_staff:
            return True
        return False


class IsNonAdminNonStaffUser(BasePermission):
    def has_permission(self, request, view):
        return not (request.user.is_staff or request.user.is_superuser)
