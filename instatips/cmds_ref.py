# Commands related to celery
# >> src/redis-server
# >> src/redis-cli ping (This command should return pong)

# >> celery -A instatips worker -l info
# >> celery -A instatips beat -l info

# >> python manage.py shell
# >> from django_celery_beat.models import PeriodicTask
# >> PeriodicTask.objects.update(last_run_at=None)
# >> python manage.py migrate

# After creating cache
# >> python manage.py createcachetable

# To list the test successes as well as failures:
# >> python manage.py test --verbosity 2
# Test coverage
# >> coverage run --source='.' manage.py test core
# >> coverage report

# View logger
# >> cat /tmp/debug.log
# To delete all content in debug.log
# >> :'%d'

# Start server using commands:
# >> sudo service postgresql start
# >> sudo -u postgres psql
# Other commands are:
# >> ALTER USER instatips_admin CREATEDB;

# >>> from django.db import connection
# >>> connection.queries
