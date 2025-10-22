"""
Django settings for portfolio project - Production Configuration
Configuración Django para el proyecto portfolio - Configuración de Producción

This file contains settings specific to the production environment.
Este archivo contiene configuraciones específicas para el entorno de producción.
"""

from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
# ADVERTENCIA DE SEGURIDAD: ¡no ejecutes con debug activado en producción!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="portfolio-production-2d83.up.railway.app",
    cast=lambda v: [s.strip() for s in v.split(",")]
)

# Database - PostgreSQL for production (Railway provides DATABASE_URL)
# Base de datos - PostgreSQL para producción (Railway proporciona DATABASE_URL)
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default=""),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Security settings for production
# Configuraciones de seguridad para producción

SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# HSTS settings (HTTP Strict Transport Security)
# Configuraciones HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging configuration for production
# Configuración de logging para producción
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

# Email configuration for production (configure with your provider)
# Configuración de correo para producción (configurar con tu proveedor)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)
