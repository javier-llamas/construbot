==================
Settings Structure
==================

Organization of Django settings for different environments.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

Construbot uses environment-based settings with inheritance to avoid duplication and support multiple environments.

**Location:** ``construbot/config/settings/``

**Files:**

- ``base.py`` - Shared settings for all environments
- ``local.py`` - Development settings
- ``test.py`` - Testing settings
- ``production.py`` - Production settings

Settings Hierarchy
==================

.. code-block:: text

   base.py (Common settings)
   ├── local.py (Development)
   ├── test.py (Testing)
   └── production.py (Production)

All environment files import from ``base.py``:

.. code-block:: python

   # local.py, test.py, production.py
   from .base import *  # Import all base settings
   from .base import env  # Import environ instance

   # Override specific settings
   DEBUG = True
   ALLOWED_HOSTS = ['localhost', '127.0.0.1']

Base Settings (base.py)
=======================

Common settings shared across all environments:

**Core Django:**

.. code-block:: python

   # Django version
   DJANGO_ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin/')

   # Internationalization
   LANGUAGE_CODE = 'es-mx'
   TIME_ZONE = 'America/Mexico_City'
   USE_I18N = True
   USE_L10N = True
   USE_TZ = True

**Installed Apps:**

.. code-block:: python

   INSTALLED_APPS = [
       # AutocompleteLight MUST be before admin
       'dal',
       'dal_select2',
       # Django contrib
       'django.contrib.admin',
       'django.contrib.auth',
       ...
       # Third-party
       'rest_framework',
       'rest_framework.authtoken',
       'allauth',
       'allauth.account',
       ...
       # Local apps
       'construbot.users',
       'construbot.proyectos',
       'construbot.api',
       'construbot.core',
   ]

.. warning::
   ``dal`` and ``dal_select2`` MUST be listed before ``django.contrib.admin`` or autocomplete widgets won't work.

**Middleware:**

.. code-block:: python

   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]

**Authentication:**

.. code-block:: python

   AUTH_USER_MODEL = 'users.User'  # Custom user model
   AUTHENTICATION_BACKENDS = [
       'construbot.core.backends.ModelBackend',  # Custom backend
       'allauth.account.auth_backends.AuthenticationBackend',
   ]

**Database (uses DATABASE_URL):**

.. code-block:: python

   DATABASES = {
       'default': env.db('DATABASE_URL'),
   }
   DATABASES['default']['ATOMIC_REQUESTS'] = True

**Static/Media Files:**

.. code-block:: python

   STATIC_ROOT = str(ROOT_DIR / 'staticfiles')
   STATIC_URL = '/static/'
   STATICFILES_DIRS = [str(APPS_DIR / 'static')]

   MEDIA_ROOT = str(APPS_DIR / 'media')
   MEDIA_URL = '/media/'

**Password Hashers:**

.. code-block:: python

   PASSWORD_HASHERS = [
       'django.contrib.auth.hashers.Argon2PasswordHasher',  # Primary
       'django.contrib.auth.hashers.PBKDF2PasswordHasher',
       'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
       'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
   ]

**Celery:**

.. code-block:: python

   if USE_TZ:
       CELERY_TIMEZONE = TIME_ZONE
   CELERY_BROKER_URL = env('CELERY_BROKER_URL', default=env('REDIS_URL', default='redis://localhost:6379/0'))
   CELERY_RESULT_BACKEND = CELERY_BROKER_URL
   CELERY_ACCEPT_CONTENT = ['json']
   CELERY_TASK_SERIALIZER = 'json'
   CELERY_RESULT_SERIALIZER = 'json'
   CELERY_TASK_TIME_LIMIT = 5 * 60  # 5 minutes
   CELERY_TASK_SOFT_TIME_LIMIT = 60  # 1 minute

Local Settings (local.py)
==========================

Development environment settings:

**Debug Mode:**

.. code-block:: python

   DEBUG = True

**Allowed Hosts:**

.. code-block:: python

   ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']

**Database:**

Can use environment variable or defaults to local PostgreSQL:

.. code-block:: python

   DATABASES = {
       'default': env.db('DATABASE_URL', default='postgresql://debug:debug@postgres:5432/construbot')
   }

**Caching (development - dummy cache):**

.. code-block:: python

   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
           'LOCATION': '',
       }
   }

**Email (console backend):**

.. code-block:: python

   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   EMAIL_HOST = 'localhost'
   EMAIL_PORT = 1025  # MailHog

**Debugging Tools:**

.. code-block:: python

   INSTALLED_APPS += ['debug_toolbar']
   MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
   INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']

**django-extensions:**

.. code-block:: python

   INSTALLED_APPS += ['django_extensions']

Test Settings (test.py)
========================

Testing environment settings:

**Debug OFF:**

.. code-block:: python

   DEBUG = False

**Database (in-memory SQLite):**

.. code-block:: python

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': ':memory:',
       }
   }

**Fast Password Hashing:**

.. code-block:: python

   PASSWORD_HASHERS = [
       'django.contrib.auth.hashers.MD5PasswordHasher',
   ]

**Templates (no caching):**

.. code-block:: python

   TEMPLATES[0]['OPTIONS']['loaders'] = [
       'django.template.loaders.filesystem.Loader',
       'django.template.loaders.app_directories.Loader',
   ]

**Email (memory backend):**

.. code-block:: python

   EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

**Celery (synchronous execution):**

.. code-block:: python

   CELERY_TASK_ALWAYS_EAGER = True
   CELERY_TASK_EAGER_PROPAGATES = True

Production Settings (production.py)
====================================

Production environment settings:

**Debug OFF:**

.. code-block:: python

   DEBUG = env.bool('DJANGO_DEBUG', False)

**Allowed Hosts:**

.. code-block:: python

   ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['example.com'])

**Security:**

.. code-block:: python

   SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
   SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   SECURE_HSTS_SECONDS = 31536000
   SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   SECURE_CONTENT_TYPE_NOSNIFF = True

**Database:**

.. code-block:: python

   DATABASES['default'] = env.db('DATABASE_URL')
   DATABASES['default']['ATOMIC_REQUESTS'] = True
   DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)

**Caching (Redis):**

.. code-block:: python

   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': env('REDIS_URL'),
           'OPTIONS': {
               'CLIENT_CLASS': 'django_redis.client.DefaultClient',
               'IGNORE_EXCEPTIONS': True,
           }
       }
   }

**Static Files (WhiteNoise):**

.. code-block:: python

   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

**Media Files (S3):**

.. code-block:: python

   if env.bool('USE_S3', default=False):
       AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
       AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
       AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
       AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')
       DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

**Email (Production service):**

.. code-block:: python

   EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='anymail.backends.mailgun.EmailBackend')

**Logging:**

.. code-block:: python

   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {
           'verbose': {
               'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
           },
       },
       'handlers': {
           'console': {
               'level': 'INFO',
               'class': 'logging.StreamHandler',
               'formatter': 'verbose'
           },
       },
       'root': {
           'level': 'INFO',
           'handlers': ['console'],
       },
   }

**Sentry:**

.. code-block:: python

   if env('SENTRY_DSN', default=None):
       import sentry_sdk
       from sentry_sdk.integrations.django import DjangoIntegration

       sentry_sdk.init(
           dsn=env('SENTRY_DSN'),
           integrations=[DjangoIntegration()],
           environment=env('SENTRY_ENVIRONMENT', default='production'),
       )

Environment Selection
=====================

**Via Environment Variable:**

.. code-block:: bash

   export DJANGO_SETTINGS_MODULE=construbot.config.settings.production
   python manage.py runserver

**Via Makefile:**

.. code-block:: bash

   make dev        # Uses local settings
   make buildprod  # Uses production settings
   make test       # Uses test settings

**In manage.py:**

.. code-block:: python

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construbot.config.settings.local')

django-environ
==============

**Loading .env file:**

.. code-block:: python

   # In base.py
   import environ

   ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
   APPS_DIR = ROOT_DIR / 'construbot'

   env = environ.Env()

   # Read .env file
   READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
   if READ_DOT_ENV_FILE:
       env.read_env(str(ROOT_DIR / '.env'))

**Accessing variables:**

.. code-block:: python

   DEBUG = env.bool('DJANGO_DEBUG', default=False)
   SECRET_KEY = env('DJANGO_SECRET_KEY')
   DATABASE_URL = env.db('DATABASE_URL')
   ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])

Library Mode
============

**CONSTRUBOT_AS_LIBRARY setting:**

When ``True``, disables standalone features:

.. code-block:: python

   # In base.py
   CONSTRUBOT_AS_LIBRARY = env.bool('CONSTRUBOT_AS_LIBRARY', default=False)

   if not CONSTRUBOT_AS_LIBRARY:
       INSTALLED_APPS += [
           'construbot.account_config',  # Only in standalone mode
       ]

**Affects:**

- Admin interface availability
- Account management URLs
- Authentication system

See :doc:`../library-mode` for details.

Best Practices
==============

**1. Never commit secrets:**

.. code-block:: bash

   # Use environment variables
   SECRET_KEY = env('DJANGO_SECRET_KEY')

   # Never hardcode:
   # SECRET_KEY = 'abc123'  # BAD!

**2. Use sensible defaults:**

.. code-block:: python

   DEBUG = env.bool('DJANGO_DEBUG', default=False)  # Safe default

**3. Document required variables:**

Create ``.env.example`` with all required variables.

**4. Validate production settings:**

.. code-block:: bash

   python manage.py check --deploy

**5. Keep base.py DRY:**

Put common settings in ``base.py``, override only what differs.

Troubleshooting
===============

**Wrong settings module loaded:**

.. code-block:: bash

   # Check current settings
   python manage.py diffsettings

   # Verify environment variable
   echo $DJANGO_SETTINGS_MODULE

**Settings not loading from .env:**

.. code-block:: bash

   # Ensure this is set
   export DJANGO_READ_DOT_ENV_FILE=True

   # Or in .env file itself (chicken-egg problem)
   # Better: export it before running Django

**Import errors:**

.. code-block:: python

   # Always import from base
   from .base import *
   from .base import env  # Don't forget this!

See Also
========

- :doc:`overview` - Architecture overview
- :doc:`../installation/configuration` - Environment configuration
- :doc:`../deployment/environment-variables` - Production variables
- `Django Settings Documentation <https://docs.djangoproject.com/en/3.2/topics/settings/>`_
