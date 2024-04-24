from api.models import CustomUser, UserTodo
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsUser(IsAuthenticated):
    def has_object_permission(self, request, view, obj: CustomUser):
        if isinstance(request.user, CustomUser):
            user = request.user
            if user.is_authenticated:
                return bool(obj.pk == user.pk)
        return False


class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj: UserTodo):
        if isinstance(request.user, CustomUser):
            user = request.user
            if user.is_authenticated:
                return bool(obj.user.pk == user.pk)
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
