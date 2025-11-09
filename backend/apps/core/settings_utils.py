import os
from distutils.util import strtobool




def env(key, default=None, cast=str):
    raw = os.getenv(key, None)
    if raw is None:
        return default
    if cast is bool:
        return bool(strtobool(raw))
    try:
        return cast(raw)
    except Exception:
        return default




# convenience wrappers


def env_bool(key, default=False):
    return env(key, default=default, cast=bool)




def env_int(key, default=0):
    return env(key, default=default, cast=int)




def choose_storage(s3_enabled: bool):
    return "storages.backends.s3boto3.S3Boto3Storage" if s3_enabled else "django.core.files.storage.FileSystemStorage"