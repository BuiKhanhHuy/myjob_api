#!/bin/bash

echo "Waiting for database..."
while ! nc -z db ${DB_PORT}; do
  sleep 1
done
echo "Database started"

echo "Waiting for redis..."
while ! nc -z redis ${SERVICE_REDIS_PORT}; do
  sleep 1
done
echo "Redis started"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000 