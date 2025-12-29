=============
Configuration
=============

Complete guide to configuring Construbot using environment variables and settings files.

Overview
========

Construbot uses a layered configuration approach:

1. **Settings files** - Python modules in ``construbot/config/settings/``
2. **Environment variables** - Loaded from ``.env`` file or system environment
3. **Runtime configuration** - Django settings controlled by environment

This follows the `Twelve-Factor App <https://12factor.net/config>`_ methodology for configuration management.

Settings Structure
==================

Settings Files
--------------

Located in ``construbot/config/settings/``:

.. code-block:: text

   settings/
   ├── __init__.py
   ├── base.py          # Shared settings for all environments
   ├── local.py         # Development settings
   ├── test.py          # Testing settings
   └── production.py    # Production settings

**Selection:**

The active settings module is controlled by ``DJANGO_SETTINGS_MODULE``:

.. code-block:: bash

   # Development
   export DJANGO_SETTINGS_MODULE=construbot.config.settings.local

   # Production
   export DJANGO_SETTINGS_MODULE=construbot.config.settings.production

**Inheritance:**

All environment-specific files inherit from ``base.py``:

.. code-block:: python

   # local.py
   from .base import *  # Import all base settings

   # Override for development
   DEBUG = True
   ALLOWED_HOSTS = ['localhost', '127.0.0.1']

Environment Variables
=====================

Loading Variables
-----------------

**From .env file (recommended for development):**

.. code-block:: bash

   # Enable .env file loading
   export DJANGO_READ_DOT_ENV_FILE=True

Create ``.env`` in project root:

.. code-block:: bash

   # .env
   DJANGO_SETTINGS_MODULE=construbot.config.settings.local
   DJANGO_DEBUG=True
   DATABASE_URL=postgresql://user:pass@localhost:5432/construbot_dev

**From system environment:**

.. code-block:: bash

   # Export variables
   export DJANGO_SETTINGS_MODULE=construbot.config.settings.production
   export DJANGO_DEBUG=False
   export DATABASE_URL=postgresql://...

**In Docker Compose:**

.. code-block:: yaml

   # docker-compose.yml
   services:
     django:
       env_file:
         - ./.env
       environment:
         - DJANGO_SETTINGS_MODULE=construbot.config.settings.local

Required Variables
==================

Core Configuration
------------------

**DJANGO_SETTINGS_MODULE**

.. code-block:: bash

   DJANGO_SETTINGS_MODULE=construbot.config.settings.local

**Values:**

- ``construbot.config.settings.local`` - Development
- ``construbot.config.settings.test`` - Testing
- ``construbot.config.settings.production`` - Production

**DJANGO_SECRET_KEY**

.. code-block:: bash

   DJANGO_SECRET_KEY=your-secret-key-here

**Generate:**

.. code-block:: bash

   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

.. warning::
   **Never commit SECRET_KEY to version control!** Use different keys for development and production.

**DJANGO_DEBUG**

.. code-block:: bash

   DJANGO_DEBUG=True   # Development
   DJANGO_DEBUG=False  # Production

.. danger::
   **Always set DEBUG=False in production!** Debug mode exposes sensitive information.

Database Configuration
----------------------

**DATABASE_URL**

.. code-block:: bash

   # PostgreSQL (recommended)
   DATABASE_URL=postgresql://user:password@host:port/database

   # Examples:
   # Local development:
   DATABASE_URL=postgresql://construbot_user:construbot_pass@localhost:5432/construbot_dev

   # Docker:
   DATABASE_URL=postgresql://debug:debug@postgres:5432/construbot

   # Production (with SSL):
   DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require

**Format:** ``postgresql://[user]:[password]@[host]:[port]/[database]``

.. note::
   Construbot uses ``django-environ`` to parse ``DATABASE_URL`` into Django's ``DATABASES`` setting.

Cache and Queue
---------------

**REDIS_URL**

.. code-block:: bash

   # Local development
   REDIS_URL=redis://localhost:6379/0

   # Docker
   REDIS_URL=redis://redis:6379/0

   # Production with password
   REDIS_URL=redis://:password@host:6379/0

**Used for:**

- Django cache backend
- Celery message broker
- Celery result backend
- Session storage (optional)

Optional Variables
==================

Email Configuration
-------------------

**Development (Console Backend):**

.. code-block:: bash

   DJANGO_EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

Emails are printed to console instead of sent.

**Production (SMTP):**

.. code-block:: bash

   DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   EMAIL_USE_TLS=True

**Using django-anymail (Recommended):**

.. code-block:: bash

   # Mailgun
   DJANGO_EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend
   MAILGUN_API_KEY=your-api-key
   MAILGUN_SENDER_DOMAIN=mg.example.com

   # SendGrid
   DJANGO_EMAIL_BACKEND=anymail.backends.sendgrid.EmailBackend
   SENDGRID_API_KEY=your-api-key

   # Amazon SES
   DJANGO_EMAIL_BACKEND=anymail.backends.amazon_ses.EmailBackend
   AWS_ACCESS_KEY_ID=your-key
   AWS_SECRET_ACCESS_KEY=your-secret
   AWS_SES_REGION_NAME=us-east-1

**Default from email:**

.. code-block:: bash

   DEFAULT_FROM_EMAIL=noreply@construbot.com
   SERVER_EMAIL=errors@construbot.com

Static and Media Files
----------------------

**Development (default):**

.. code-block:: bash

   # Static files served by Django
   # Media files served from MEDIA_ROOT

**Production (S3):**

.. code-block:: bash

   # AWS S3 for media files
   USE_S3=True
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_STORAGE_BUCKET_NAME=your-bucket-name
   AWS_S3_REGION_NAME=us-east-1

   # Optional: Custom domain
   AWS_S3_CUSTOM_DOMAIN=cdn.example.com

**Static files (WhiteNoise):**

No configuration needed. WhiteNoise is enabled by default in production settings.

Allowed Hosts
-------------

**DJANGO_ALLOWED_HOSTS**

.. code-block:: bash

   # Development
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

   # Production (comma-separated)
   DJANGO_ALLOWED_HOSTS=example.com,www.example.com,api.example.com

.. warning::
   **Required in production!** Django will refuse connections from hosts not in this list.

CORS Configuration
------------------

**CORS_ALLOWED_ORIGINS**

.. code-block:: bash

   # Allow specific origins (recommended)
   CORS_ALLOWED_ORIGINS=https://app.example.com,https://mobile.example.com

**CORS_ALLOW_ALL_ORIGINS**

.. code-block:: bash

   # Development only - allow all origins
   CORS_ALLOW_ALL_ORIGINS=True

.. danger::
   **Never use CORS_ALLOW_ALL_ORIGINS in production!** Only allow trusted origins.

Docker Configuration
--------------------

**USE_DOCKER**

.. code-block:: bash

   USE_DOCKER=yes  # Docker environment
   USE_DOCKER=no   # Local environment

This affects:

- Database host (``postgres`` vs ``localhost``)
- Redis host (``redis`` vs ``localhost``)
- Email host (``mailhog`` vs localhost SMTP)

Library Mode
------------

**CONSTRUBOT_AS_LIBRARY**

.. code-block:: bash

   CONSTRUBOT_AS_LIBRARY=False  # Standalone mode (default)
   CONSTRUBOT_AS_LIBRARY=True   # Library mode

When ``True``:

- Disables admin interface
- Disables account management URLs
- Disables standalone authentication
- Use Construbot as Django app in your project

See :doc:`../library-mode` for details.

Sentry Integration
------------------

**SENTRY_DSN**

.. code-block:: bash

   SENTRY_DSN=https://your-dsn@sentry.io/project-id

**SENTRY_ENVIRONMENT**

.. code-block:: bash

   SENTRY_ENVIRONMENT=production  # or staging, development

**SENTRY_SAMPLE_RATE**

.. code-block:: bash

   # 1.0 = 100% of errors sent to Sentry
   SENTRY_SAMPLE_RATE=1.0

Logging
-------

**LOG_LEVEL**

.. code-block:: bash

   LOG_LEVEL=INFO   # Production
   LOG_LEVEL=DEBUG  # Development

**Values:** DEBUG, INFO, WARNING, ERROR, CRITICAL

Celery Configuration
--------------------

**CELERY_BROKER_URL**

.. code-block:: bash

   CELERY_BROKER_URL=redis://redis:6379/0

Usually same as ``REDIS_URL``.

**CELERY_RESULT_BACKEND**

.. code-block:: bash

   CELERY_RESULT_BACKEND=redis://redis:6379/0

**CELERY_TASK_ALWAYS_EAGER**

.. code-block:: bash

   # Execute tasks synchronously (testing)
   CELERY_TASK_ALWAYS_EAGER=True

Configuration by Environment
=============================

Development (.env)
------------------

Complete ``.env`` file for local development:

.. code-block:: bash

   # Django Settings
   DJANGO_SETTINGS_MODULE=construbot.config.settings.local
   DJANGO_DEBUG=True
   DJANGO_READ_DOT_ENV_FILE=True
   DJANGO_SECRET_KEY=dev-secret-key-change-in-production

   # Docker
   USE_DOCKER=yes  # Set to 'no' for local development

   # Database (Docker)
   DATABASE_URL=postgresql://debug:debug@postgres:5432/construbot

   # Database (Local)
   # DATABASE_URL=postgresql://construbot_user:construbot_pass@localhost:5432/construbot_dev

   # Redis
   REDIS_URL=redis://redis:6379/0

   # Email (Console)
   DJANGO_EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

   # Celery
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0

   # Allowed Hosts
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

   # CORS (Development only)
   CORS_ALLOW_ALL_ORIGINS=True

Testing
-------

Environment for running tests:

.. code-block:: bash

   # Settings
   DJANGO_SETTINGS_MODULE=construbot.config.settings.test
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=test-secret-key

   # Database (in-memory SQLite)
   # No DATABASE_URL needed - test settings use SQLite

   # Celery (synchronous execution)
   CELERY_TASK_ALWAYS_EAGER=True

Production
----------

Production environment variables:

.. code-block:: bash

   # Django Settings
   DJANGO_SETTINGS_MODULE=construbot.config.settings.production
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=<generate-strong-secret-key>

   # Security
   DJANGO_SECURE_SSL_REDIRECT=True
   DJANGO_SECURE_HSTS_SECONDS=31536000
   DJANGO_SESSION_COOKIE_SECURE=True
   DJANGO_CSRF_COOKIE_SECURE=True

   # Database (with SSL)
   DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require

   # Redis
   REDIS_URL=redis://:password@host:6379/0

   # Email (Production service)
   DJANGO_EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend
   MAILGUN_API_KEY=<your-api-key>
   MAILGUN_SENDER_DOMAIN=mg.example.com
   DEFAULT_FROM_EMAIL=noreply@example.com

   # Static/Media Files (S3)
   USE_S3=True
   AWS_ACCESS_KEY_ID=<your-key>
   AWS_SECRET_ACCESS_KEY=<your-secret>
   AWS_STORAGE_BUCKET_NAME=construbot-media
   AWS_S3_REGION_NAME=us-east-1

   # Allowed Hosts (comma-separated)
   DJANGO_ALLOWED_HOSTS=example.com,www.example.com,api.example.com

   # CORS (specific origins only)
   CORS_ALLOWED_ORIGINS=https://app.example.com

   # Sentry
   SENTRY_DSN=<your-sentry-dsn>
   SENTRY_ENVIRONMENT=production

   # Logging
   LOG_LEVEL=INFO

Security Settings
=================

Production Security Checklist
------------------------------

.. code-block:: bash

   # HTTPS Enforcement
   DJANGO_SECURE_SSL_REDIRECT=True
   DJANGO_SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https

   # HSTS (HTTP Strict Transport Security)
   DJANGO_SECURE_HSTS_SECONDS=31536000
   DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
   DJANGO_SECURE_HSTS_PRELOAD=True

   # Cookie Security
   DJANGO_SESSION_COOKIE_SECURE=True
   DJANGO_SESSION_COOKIE_HTTPONLY=True
   DJANGO_CSRF_COOKIE_SECURE=True
   DJANGO_CSRF_COOKIE_HTTPONLY=True

   # Content Security
   DJANGO_SECURE_CONTENT_TYPE_NOSNIFF=True
   DJANGO_SECURE_BROWSER_XSS_FILTER=True
   X_FRAME_OPTIONS=DENY

**Run security check:**

.. code-block:: bash

   python manage.py check --deploy

Managing Configuration
======================

Environment File Template
--------------------------

Create ``.env.example`` as a template:

.. code-block:: bash

   # Copy for local use: cp .env.example .env

   # Django
   DJANGO_SETTINGS_MODULE=construbot.config.settings.local
   DJANGO_DEBUG=True
   DJANGO_SECRET_KEY=change-me

   # Database
   DATABASE_URL=postgresql://user:pass@host:port/database

   # ... (include all required variables with examples)

**Benefits:**

- Documents required variables
- Provides examples for developers
- Safe to commit (no secrets)

Secrets Management
------------------

**Development:**

- Use ``.env`` file (git-ignored)
- Share ``.env.example`` template

**Production:**

- Use environment variables (not .env file)
- Store secrets in secure vault (AWS Secrets Manager, HashiCorp Vault)
- Inject secrets at runtime

**Example with AWS Secrets Manager:**

.. code-block:: python

   # In settings/production.py
   import boto3
   import json

   def get_secret(secret_name):
       client = boto3.client('secretsmanager')
       response = client.get_secret_value(SecretId=secret_name)
       return json.loads(response['SecretString'])

   secrets = get_secret('construbot/production')
   SECRET_KEY = secrets['DJANGO_SECRET_KEY']
   DATABASE_URL = secrets['DATABASE_URL']

Validating Configuration
-------------------------

**Check required variables:**

.. code-block:: bash

   # Django checks
   python manage.py check

   # Deployment checks
   python manage.py check --deploy

   # Database connection
   python manage.py dbshell

**Test email configuration:**

.. code-block:: bash

   python manage.py shell

.. code-block:: python

   >>> from django.core.mail import send_mail
   >>> send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])

Troubleshooting
===============

Common Issues
-------------

**"ImproperlyConfigured: Set the DATABASE_URL environment variable"**

.. code-block:: bash

   # Ensure DATABASE_URL is set
   echo $DATABASE_URL

   # Or add to .env
   DATABASE_URL=postgresql://...

**"SECRET_KEY is required"**

.. code-block:: bash

   # Generate and set SECRET_KEY
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

   # Add to .env
   DJANGO_SECRET_KEY=<generated-key>

**"CommandError: You must set settings.ALLOWED_HOSTS"**

.. code-block:: bash

   # Add to .env
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

**"DisallowedHost at /"**

.. code-block:: bash

   # Add your domain to ALLOWED_HOSTS
   DJANGO_ALLOWED_HOSTS=example.com,www.example.com

**Variables not loading from .env**

.. code-block:: bash

   # Ensure this is set
   DJANGO_READ_DOT_ENV_FILE=True

   # Check .env is in project root (same directory as manage.py)
   ls -la .env

Variable Precedence
-------------------

If a variable is set in multiple places, this is the priority order:

1. **System environment variables** (highest priority)
2. **.env file**
3. **Settings file defaults** (lowest priority)

Example:

.. code-block:: bash

   # .env
   DJANGO_DEBUG=True

   # Terminal
   export DJANGO_DEBUG=False

   # Django will use DEBUG=False (system environment wins)

See Also
========

- :doc:`docker-setup` - Docker environment configuration
- :doc:`local-setup` - Local environment configuration
- :doc:`../deployment/environment-variables` - Production environment setup
- :doc:`../architecture/settings-structure` - Settings file organization
- `Django Settings Best Practices <https://docs.djangoproject.com/en/3.2/topics/settings/>`_
- `Twelve-Factor App Config <https://12factor.net/config>`_
