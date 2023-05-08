#!/bin/sh

while ! nc -z $DB_HOST $DB_PORT; do
  echo "Wait for DB connection..."
  sleep 1
done

alembic upgrade head

exec "$@"
