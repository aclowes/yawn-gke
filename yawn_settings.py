import dj_database_url
from importlib.metadata import version

from yawn.settings.base import *

# this uses DATABASE_URL env variable:

DATABASES['default'] = dj_database_url.config(conn_max_age=600)

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

# Allow anonymous read
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
    'rest_framework.permissions.IsAuthenticatedOrReadOnly',
]

INSTALLED_APPS += ['raven.contrib.django']

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
    'release': version("yawns"),
    'name': os.environ.get('KUBERNETES_POD_NAME'),
    'include_paths': ['yawn'],
}
