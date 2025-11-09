import os
from django.conf import settings




def safe_join(base: str, *paths: str) -> str:
    candidate = os.path.normpath(os.path.join(base, *paths))
    base_norm = os.path.normpath(base)
    if not candidate.startswith(base_norm):
        raise ValueError("Attempt to escape base path")
    return candidate




def upload_to_instance(instance, filename: str) -> str:
    model = instance.__class__.__name__.lower()
    return os.path.join(model, filename)