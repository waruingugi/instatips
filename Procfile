web: gunicorn instatips.wsgi --log-file -
worker: celery -A instatips worker -l info
beat: celery -A instatips beat -l info