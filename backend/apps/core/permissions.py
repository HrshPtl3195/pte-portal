# backend/apps/core/permissions.py
from typing import Any

from rest_framework.permissions import BasePermission # type: ignore

from .constants import Role


class IsAdmin(BasePermission):
    """
    Permission that grants access to admin users.

    Criteria (any of):
      - user.is_superuser == True
      - user.is_staff == True
      - user.role == Role.ADMIN.value

    Also requires the user to be authenticated.
    """

    def has_permission(self, request: Any, view: Any) -> bool:
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False

        # Standard Django admin flags take precedence
        if getattr(user, "is_superuser", False) or getattr(user, "is_staff", False):
            return True

        # Fall back to role enum if present on user
        user_role = getattr(user, "role", None)
        admin_role_val = getattr(Role.ADMIN, "value", Role.ADMIN)
        return user_role == admin_role_val


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission to allow owners of an object or admins.

    has_permission:
      - requires an authenticated user (object-level checks do the real work).

    has_object_permission:
      - returns True if:
          * user is admin (IsAdmin-style logic)
          * OR object's owner id matches request.user.id
    """

    def has_permission(self, request: Any, view: Any) -> bool:
        # require authentication for any object-level flow
        user = getattr(request, "user", None)
        return bool(user and getattr(user, "is_authenticated", False))

    def has_object_permission(self, request: Any, view: Any, obj: Any) -> bool:
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False

        # Admins always allowed
        if getattr(user, "is_superuser", False) or getattr(user, "is_staff", False):
            return True

        # Check role enum as alternative admin indicator
        user_role = getattr(user, "role", None)
        if user_role == getattr(Role.ADMIN, "value", Role.ADMIN):
            return True

        # Flexible owner detection: owner_id, owner (object or id), created_by
        owner_id = None
        if hasattr(obj, "owner_id"):
            owner_id = getattr(obj, "owner_id")
        elif hasattr(obj, "owner"):
            owner = getattr(obj, "owner")
            owner_id = getattr(owner, "id", owner)
        elif hasattr(obj, "created_by"):
            cb = getattr(obj, "created_by")
            owner_id = getattr(cb, "id", cb)

        # If ownership cannot be determined, deny by default
        if owner_id is None:
            return False

        return getattr(user, "id", None) == owner_id
