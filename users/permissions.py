from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Права для владельца"""
    message = "Вы не являетесь владельцем"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsUserOwner(BasePermission):
    """Права доступа для пользователя"""
    message = "Вы не являетесь владельцем этой учетной записи"

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.pk
