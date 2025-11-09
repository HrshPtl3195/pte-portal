from functools import wraps
from .exceptions import PermissionDeniedError
from .constants import Role




def require_role(role: Role):
    def deco(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            user = getattr(request, "user", None)
            if not user or not getattr(user, "role", None) == role.value:
                raise PermissionDeniedError()
            return view(request, *args, **kwargs)


        return wrapped


    return deco