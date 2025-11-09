from rest_framework.permissions import BasePermission
from .constants import Role




class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user, "role", None) == Role.ADMIN.value)




class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and getattr(request.user, "role", None) == Role.ADMIN.value:
            return True
        return getattr(obj, "owner_id", None) == getattr(request.user, "id", None)