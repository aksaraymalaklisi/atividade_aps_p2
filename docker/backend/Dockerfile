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
## Ensure staticfiles and media directories exist and are writable by the non-root user
RUN mkdir -p /app/staticfiles /app/media && chown -R appuser:appgroup /app/staticfiles /app/media || true

COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh

# Collect static files
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# Switch to non-root user
USER appuser
ENTRYPOINT ["/app/docker-entrypoint.sh"]

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "from urllib.request import Request, urlopen; req=Request('http://127.0.0.1:8000/api/health/'); req.add_header('Host', 'api.aksaraymalaklisi.net'); urlopen(req)" || exit 1

CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "120"]
