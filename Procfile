web: gunicorn myjob_api.wsgi --log-file -
migrate: python manage.py migrate
collectstatic: python manage.py collectstatic --noinput
worker: celery -A myjob_api.celery worker --loglevel=info
beat: celery -A myjob_api.celery beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
