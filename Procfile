web: gunicorn myjob_api.wsgi --log-file -
worker: celery -A myjob_api.celery worker --pool=solo --loglevel=info