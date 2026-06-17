"""
Production-specific Django settings.

Validates that all required environment variables are set.
Fails fast on startup with clear error messages if anything is missing.
"""

import os

from core.env import optional_env, require_env

from .base import *  # noqa: F403

# --- Security ---

SECRET_KEY = require_env("SECRET_KEY", description="Django secret key for cryptographic signing")

DEBUG = False

ALLOWED_HOSTS = require_env(
    "ALLOWED_HOSTS",
    description="Comma-separated list of allowed hostnames",
).split(",")

# --- CORS ---

CORS_ALLOWED_ORIGINS = require_env(
    "CORS_ALLOWED_ORIGINS",
    description="Comma-separated list of allowed frontend origins (e.g. https://petadopt.example.com)",
).split(",")

# Validate CORS origins: ensure each entry is a non-empty URL starting with http:// or https://
_raw_cors = CORS_ALLOWED_ORIGINS
_validated_origins = []
for _o in _raw_cors:
    _s = _o.strip()
    if not _s:
        continue
    if not (_s.startswith("http://") or _s.startswith("https://")):
        raise ValueError(
            "Invalid CORS origin '%s'. Each origin must be a full URL starting with http:// or https://."
            % _s
        )
    _validated_origins.append(_s)

CORS_ALLOWED_ORIGINS = _validated_origins
# --- Database ---
# In production, DATABASE_URL components can be overridden individually.
# The base.py defaults point to 'db:5432' which works within Docker Compose.
# Override POSTGRES_HOST, POSTGRES_PORT, etc. if the database is on another machine.

# --- Static Files ---

STATIC_ROOT = os.getenv("STATIC_ROOT", "/app/staticfiles")

# --- Logging ---

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": '{"time": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# --- Optional integrations ---

SENTRY_DSN = optional_env("SENTRY_DSN", description="Sentry DSN for error tracking")
if SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=0.1)
