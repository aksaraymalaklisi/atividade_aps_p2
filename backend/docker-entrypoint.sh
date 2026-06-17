#!/bin/sh

set -e

show_error() {
  echo "[backend entrypoint] ERROR: $1" >&2
}

require_env() {
  # POSIX-compatible indirect expansion (works with /bin/sh)
  eval _val="\$$1"
  if [ -z "$_val" ]; then
    show_error "Required environment variable $1 is not set."
    exit 1
  fi
}

require_env "SECRET_KEY"
require_env "ALLOWED_HOSTS"
require_env "CORS_ALLOWED_ORIGINS"
require_env "POSTGRES_PASSWORD"

POSTGRES_HOST=${POSTGRES_HOST:-db}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
POSTGRES_DB=${POSTGRES_DB:-petadopt}
POSTGRES_USER=${POSTGRES_USER:-postgres}

export POSTGRES_HOST POSTGRES_PORT POSTGRES_DB POSTGRES_USER

printf "[backend entrypoint] Waiting for database at %s:%s..." "$POSTGRES_HOST" "$POSTGRES_PORT"

until python - <<'PY'
import os
import sys
import psycopg

try:
    conn = psycopg.connect(
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        dbname=os.environ['POSTGRES_DB'],
        connect_timeout=3,
    )
    conn.close()
except Exception:
    sys.exit(1)
PY
 do
  printf '.'
  sleep 1
 done

printf '\n'

echo "[backend entrypoint] Running migrations..."
python manage.py migrate --noinput

echo "[backend entrypoint] Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
