# portal_settings/base.py
from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECRET_KEY = 'django-insecure-hrum!ljy##hz+xe-r5nzaj%zdkq_zxnvq133lhb+)$@l!z_=gi'
# DEBUG = True

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = False
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party
    "rest_framework",
    "drf_spectacular",

    # local apps
    "apps.core",
    "apps.accounts",
    "apps.test_engine",
    "apps.speaking",
    "apps.writing",
    "apps.listening",
    "apps.reading",
    "apps.media",
    "apps.transcription",
    "apps.scoring",
    "apps.human_evaluator",
    "apps.mock_tests",
    "apps.content_management",
    "apps.notifications",
    "apps.analytics",
    "apps.admin_panel",
    "apps.support",
    "apps.search",
    "apps.audit",
    "apps.i18n",
    "apps.feature_flags",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Attach request_id and per-request logger early so downstream code sees it
    'apps.core.middleware.RequestIDMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Catch-all JSON error middleware for API routes (keep near end so request.user exists)
    'apps.core.middleware.ExceptionToJSONMiddleware',
]

ROOT_URLCONF = 'portal_settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {"context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    },
]

WSGI_APPLICATION = 'portal_settings.wsgi.application'
ASGI_APPLICATION = "portal_settings.asgi.application"


env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
        'OPTIONS': {
            'options': '-c search_path=accounts,core,test_engine,mock_tests,public'
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.SessionAuthentication",),
    "EXCEPTION_HANDLER": "apps.core.exceptions.drf_exception_handler",
    # optionally set default pagination class later:
    # "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.StandardPagination",
}
REST_FRAMEWORK["DEFAULT_PAGINATION_CLASS"] = "apps.core.pagination.StandardPagination"
REST_FRAMEWORK["PAGE_SIZE"] = 20

SPECTACULAR_SETTINGS = {
    'TITLE': 'PTE Portal API',
    'DESCRIPTION': 'API documentation for PTE Portal backend',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# ------------------------
# LOGGING (uses apps.core.logging.RequestIDFilter)
# ------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        # JSON formatter (pythonjsonlogger) - includes request_id in structured output
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            # include request_id as a named field so RequestIDFilter can set it
            "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s",
        },
        "simple": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"},
    },
    "filters": {
        # Use the RequestIDFilter defined in apps.core.logging which ensures
        # every log record has a 'request_id' attribute (fallback '-').
        "request_id_filter": {
            "()": "apps.core.logging.RequestIDFilter",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "filters": ["request_id_filter"],
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "INFO", "propagate": False},
        # Optionally add an 'apps' logger for your application logs
        "apps": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
