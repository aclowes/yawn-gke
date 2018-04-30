import dj_database_url

from yawn.settings.base import *

# this uses DATABASE_URL env variable:

DATABASES['default'] = dj_database_url.config(conn_max_age=600)

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = [os.environ('ALLOWED_HOSTS')]

# Allow anonymous read
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
    'rest_framework.permissions.IsAuthenticatedOrReadOnly',
]
