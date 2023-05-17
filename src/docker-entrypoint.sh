#!/bin/sh

while ! nc -z $DB_HOST $DB_PORT; do
  echo "Wait for DB connection..."
  sleep 1
done

alembic -c /app/alembic.ini upgrade head && gunicorn -k uvicorn.workers.UvicornWorker main:app --bind=${PROFILE_APP_HOST}:${PROFILE_APP_PORT}

exec "$@"
