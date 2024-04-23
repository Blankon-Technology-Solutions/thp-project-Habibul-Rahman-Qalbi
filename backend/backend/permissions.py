from rest_framework.permissions import BasePermission, IsAuthenticated
from api.models import CustomUser


class IsUser(IsAuthenticated):
    def has_object_permission(self, request, view, obj: CustomUser):
        if isinstance(request.user, CustomUser):
            user = request.user
            if user.is_authenticated:
                return bool(obj.email == user.email)
        return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, CustomUser):
            user = request.user
            if user.is_authenticated:
                return user.is_staff or user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        if isinstance(request.user, CustomUser):
            user = request.user
            if user.is_authenticated:
                return user.is_staff or user.is_superuser
        return False
