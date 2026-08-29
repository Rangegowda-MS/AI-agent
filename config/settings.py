from pathlib import Path
import os
from dotenv import load_dotenv

# =========================================================
# BASE
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-only-secret-key-change-this-in-production"
)

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "ai-travel-agent-e7mp.onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "travel",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise must stay directly after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URLS / WSGI / ASGI
# =========================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================================
# DATABASE
# =========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = []


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# Django 5 + WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# DJANGO REST FRAMEWORK
# =========================================================

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}


# =========================================================
# AI CONFIGURATION
# =========================================================

AI_PROVIDER = os.getenv("AI_PROVIDER", "mock")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


# =========================================================
# RENDER / HTTPS SETTINGS
# =========================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG