#!/bin/sh
set -e

# check postgres readiness
echo "Waiting for Postgres..."
while ! nc -z db 5432; do
  sleep 0.2
done
echo "PostgreSQL is up"

# Add redis check readiness
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.2
done
echo "Redis is up"

echo "Running DB setup..."
python manage.py create_db || true

echo "Starting Flask..."
exec flask --app manage.py run --host=0.0.0.0 --port=5000

