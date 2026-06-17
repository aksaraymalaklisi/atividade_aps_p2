"""
Development-specific Django settings.

Uses safe defaults for all configuration — no environment variables required.
The compose.dev.yml provides PostgreSQL automatically.
"""

from .base import *  # noqa: F403

# --- Security ---

INSTALLED_APPS += ["behave_django"]  # noqa: F405

SECRET_KEY = "django-insecure-dev-only-key-do-not-use-in-production"

DEBUG = True

ALLOWED_HOSTS = ["*"]

# --- CORS ---
# Allow all origins in development (frontend on localhost:5173)

CORS_ALLOW_ALL_ORIGINS = True

# --- Database ---
# Defaults from base.py already point to localhost:5432 with postgres/postgres.
# The compose.dev.yml provides a PostgreSQL container matching these defaults.
# If running outside Docker, start the DB with:
#   docker compose -f compose.dev.yml up db

# --- Logging ---

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
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
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
