#!/bin/sh

while ! nc -z $DB_HOST $DB_PORT; do
  echo "Wait for DB connection..."
  sleep 1
done

alembic -c /app/alembic.ini upgrade head && python cli.py ugc-actions-consumer-start

exec "$@"
