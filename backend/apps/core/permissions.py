# apps/core/permissions.py
from rest_framework.permissions import BasePermission
from typing import Any

from .constants import Role
from .exceptions import PermissionDeniedError

class IsAdmin(BasePermission):
    """
    Require authenticated user and role == Role.ADMIN.value
    """

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False
        # Role can be a string on the user (preferred) or you can adapt to your user model
        user_role = getattr(user, "role", None)
        # Support both Enum value or Enum instance
        if hasattr(Role, "value"):
            expected = Role.ADMIN.value if hasattr(Role.ADMIN, "value") else Role.ADMIN
        else:
            expected = Role.ADMIN
        return user_role == expected


class IsOwnerOrAdmin(BasePermission):
    """
    Allow owner of object or admin users. Requires authentication.
    Expects the view's get_object() to return an object with `owner_id` or `owner` attribute.
    """

    def has_permission(self, request, view) -> bool:
        # Block anonymous users immediately
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False
        # Allow safe-list operations to be handled by view if needed, but default allow
        return True

    def has_object_permission(self, request, view, obj: Any) -> bool:
        user = request.user
        # Admins always win
        if getattr(user, "role", None) == getattr(Role.ADMIN, "value", Role.ADMIN):
            return True

        # Try to detect ownership, flexible about attribute names
        owner_id = None
        if hasattr(obj, "owner_id"):
            owner_id = getattr(obj, "owner_id")
        elif hasattr(obj, "owner"):
            owner = getattr(obj, "owner")
            # owner might be a user instance or an id
            owner_id = getattr(owner, "id", owner)

        if owner_id is None:
            # If ownership cannot be determined, deny by default
            return False

        return getattr(user, "id", None) == owner_id
