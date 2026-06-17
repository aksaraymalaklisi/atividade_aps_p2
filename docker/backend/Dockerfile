# =============================================================================
# PetAdopt Backend — Multi-stage Dockerfile
# =============================================================================
# Stages:
#   - base:        System dependencies and non-root user
#   - development: Dev server with hot-reload + dev dependencies
#   - production:  Gunicorn with optimized image (Phase 6)
# =============================================================================

# --- Stage: base ---
FROM python:3.14-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies for psycopg (PostgreSQL driver)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# --- Stage: development ---
FROM base AS development

COPY requirements/base.txt requirements/base.txt
COPY requirements/development.txt requirements/development.txt
RUN pip install --no-cache-dir -r requirements/development.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# --- Stage: production ---
FROM base AS production

COPY requirements/base.txt requirements/base.txt
COPY requirements/production.txt requirements/production.txt
RUN pip install --no-cache-dir -r requirements/production.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# Switch to non-root user
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health/')" || exit 1

CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "120"]
