"""
Django settings for Sparsh Inclusive Education public website.
"""
from pathlib import Path
import os
import sys

import pymysql
from dotenv import load_dotenv

# PyMySQL provides Django's MySQLdb interface without a C compiler,
# which shared hosting such as GoDaddy cPanel usually does not allow.
pymysql.install_as_MySQLdb()
pymysql.version_info = (2, 2, 1, "final", 0)

import dj_database_url

from apps.core.mail import resolve_smtp_security

# backend/config/settings.py → backend/ → project root
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "dev-only-insecure-key-change-in-production-sparsh-2026",
)

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1",
    ).split(",")
    if h.strip()
]
if DEBUG:
    for host in ("testserver", "localhost", "127.0.0.1"):
        if host not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(host)

# Optional hostname injected by a platform. GoDaddy does not set this.
EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
if EXTERNAL_HOSTNAME and EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if o.strip()
]
if EXTERNAL_HOSTNAME:
    external_origin = f"https://{EXTERNAL_HOSTNAME}"
    if external_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(external_origin)

# Trust the hosting proxy's HTTPS marker (Apache on GoDaddy, or a similar proxy).
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "apps.core",
    "apps.programs",
    "apps.admissions",
    "apps.people",
    "apps.content",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_ROOT / "frontend" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database: tests use SQLite. Production uses MySQL when DB_NAME is set
# (GoDaddy cPanel). A mysql:// DATABASE_URL is also accepted. Anything else,
# including an old PostgreSQL URL, falls back to local SQLite.
_database_url = os.getenv("DATABASE_URL", "").strip()
if "test" in sys.argv:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
elif os.getenv("DB_NAME", "").strip():
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME").strip(),
            "USER": os.getenv("DB_USER", "").strip(),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost").strip() or "localhost",
            "PORT": os.getenv("DB_PORT", "3306").strip() or "3306",
            "CONN_MAX_AGE": 0,
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
elif _database_url.startswith(("mysql://", "mysql2://")):
    DATABASES = {
        "default": dj_database_url.config(
            default=_database_url,
            conn_max_age=0,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [PROJECT_ROOT / "frontend" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}
WHITENOISE_MANIFEST_STRICT = False

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

def _env_flag(name, default="false"):
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")


def _env_int(name, default):
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


# Console backend until EMAIL_BACKEND is set to Django's SMTP backend.
# Titan Mail: smtpout.secureserver.net, port 465, SSL only (not STARTTLS).
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "").strip()
EMAIL_PORT = _env_int("EMAIL_PORT", 465)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "").strip()
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_SSL, EMAIL_USE_TLS = resolve_smtp_security(
    EMAIL_PORT,
    _env_flag("EMAIL_USE_SSL"),
    _env_flag("EMAIL_USE_TLS"),
)
EMAIL_TIMEOUT = _env_int("EMAIL_TIMEOUT", 20)
# Titan accepts mail only from the authenticated mailbox or one of its aliases.
DEFAULT_FROM_EMAIL = (
    os.getenv("DEFAULT_FROM_EMAIL", "").strip()
    or EMAIL_HOST_USER
    or "noreply@sparshinclusiveeducation.com"
)
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "enquiry@sparshinclusiveeducation.com")
ADMISSIONS_NOTIFY_EMAIL = os.getenv(
    "ADMISSIONS_NOTIFY_EMAIL", "enquiry@sparshinclusiveeducation.com"
)
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "9600163526")

RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY", "")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY", "")

SITE_NAME = "Sparsh Inclusive Education"
SITE_TAGLINE = "Different Abilities. Infinite Possibilities."
SITE_URL = os.getenv("SITE_URL", "https://sparshinclusive.edu")

# Security headers (active when DEBUG is False)
if not DEBUG:
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() in (
        "1",
        "true",
        "yes",
    )
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
elif EXTERNAL_HOSTNAME:
    # HTTPS cookies when a public hostname is configured, even if DEBUG is on.
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "apps": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "sparsh-cache",
        "TIMEOUT": 300,
    }
}
