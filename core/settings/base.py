"""
Django settings for portfolio project - Base Configuration
Configuración Django para el proyecto portfolio - Configuración Base

This file contains settings common to all environments.
Este archivo contiene configuraciones comunes a todos los entornos.
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Construir rutas dentro del proyecto así: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# ADVERTENCIA DE SEGURIDAD: ¡mantén la clave secreta en producción secreta!
SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-this-in-production")

# Application definition
# Definición de aplicaciones

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps - Apps de terceros
    "rest_framework",
    "corsheaders",
    "drf_spectacular",  # API documentation
    # Local apps - Apps locales
    "apps.projects",
    "apps.skills",
    "apps.about",
    "apps.contact",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # For static files in production
    "corsheaders.middleware.CorsMiddleware",  # CORS middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Password validation
# Validación de contraseñas
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# Internacionalización
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "es-es"

TIME_ZONE = "America/Mexico_City"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise configuration for static files
# Configuración de WhiteNoise para archivos estáticos
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (User uploaded content)
# Archivos multimedia (Contenido subido por usuarios)
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# Tipo de campo de clave primaria predeterminado
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework configuration
# Configuración de Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    # API Schema - Esquema de API
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Convention: Use camelCase in JSON responses (not snake_case)
    # Convención: Usar camelCase en respuestas JSON (no snake_case)
    "JSON_UNDERSCOREIZE": {
        "no_underscore_before_number": True,
    },
}

# CORS configuration
# Configuración de CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

# Custom settings for camelCase convention in JSON responses
# Configuraciones personalizadas para convención camelCase en respuestas JSON

# Email configuration (to be overridden in environment-specific settings)
# Configuración de correo (para ser sobrescrita en configuraciones específicas del entorno)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# DRF Spectacular configuration
# Configuración de DRF Spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "Portfolio API",
    "DESCRIPTION": "API REST para el portafolio personal. Incluye endpoints para proyectos, habilidades, información personal y mensajes de contacto. / REST API for personal portfolio. Includes endpoints for projects, skills, personal information and contact messages.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # Camel case convention for JSON responses
    # Convención camel case para respuestas JSON
    "CAMELIZE_NAMES": True,
    "COMPONENT_SPLIT_REQUEST": True,
    # Language configuration - Configuración de idioma
    "LANGUAGE": "es-ES",
    # Schema generation - Generación de esquema
    "SCHEMA_PATH_PREFIX": "/api/",
    "SERVERS": [
        {"url": "http://localhost:8000", "description": "Desarrollo local / Local development"},
        {"url": "https://api.portfolio.com", "description": "Producción / Production"},
    ],
    # Contact information - Información de contacto
    "CONTACT": {
        "name": "Portfolio API Support",
        "email": "support@portfolio.com",
    },
    "LICENSE": {
        "name": "MIT License",
    },
}
