=====================
Environment Variables
=====================

Complete reference for all environment variables used in production deployments.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

Construbot uses environment variables for configuration following the `Twelve-Factor App <https://12factor.net/config>`_ methodology. Variables are loaded from:

1. ``.env`` file (development/Docker)
2. System environment (production servers)
3. Container environment (Docker/Kubernetes)

.. note::
   This document focuses on **production-specific** variables. For development configuration, see :doc:`../installation/configuration`.

Required Variables
==================

Django Core
-----------

DJANGO_SETTINGS_MODULE
^^^^^^^^^^^^^^^^^^^^^^^

**Type:** String

**Required:** Yes

**Description:** Python path to settings module

**Production value:**

.. code-block:: bash

   DJANGO_SETTINGS_MODULE=construbot.config.settings.production

**Values:**

- ``construbot.config.settings.local`` - Development
- ``construbot.config.settings.test`` - Testing
- ``construbot.config.settings.production`` - Production

DJANGO_SECRET_KEY
^^^^^^^^^^^^^^^^^^

**Type:** String (50+ characters)

**Required:** Yes

**Description:** Cryptographic signing key for sessions, cookies, CSRF tokens

.. danger::
   **Never commit SECRET_KEY to version control!** Use different keys for dev/prod.

**Generate:**

.. code-block:: bash

   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

**Example:**

.. code-block:: bash

   DJANGO_SECRET_KEY=django-insecure-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0

DJANGO_DEBUG
^^^^^^^^^^^^

**Type:** Boolean

**Required:** Yes

**Description:** Enable/disable debug mode

.. danger::
   **MUST be False in production!** Debug mode exposes sensitive information.

**Production value:**

.. code-block:: bash

   DJANGO_DEBUG=False

**Effects when True:**

- Detailed error pages with tracebacks
- Exposes settings and environment variables
- Shows SQL queries
- Serves static files via Django (slow)
- Disables template caching

DJANGO_ALLOWED_HOSTS
^^^^^^^^^^^^^^^^^^^^^

**Type:** Comma-separated string

**Required:** Yes (when DEBUG=False)

**Description:** Hosts/domains that Django serves

**Example:**

.. code-block:: bash

   DJANGO_ALLOWED_HOSTS=example.com,www.example.com,api.example.com

**Include:**

- Root domain
- www subdomain
- API subdomain (if separate)
- Load balancer hostname

**Validation:**

.. code-block:: python

   # Test in shell
   from django.conf import settings
   print(settings.ALLOWED_HOSTS)
   # ['example.com', 'www.example.com', 'api.example.com']

Database
--------

DATABASE_URL
^^^^^^^^^^^^

**Type:** PostgreSQL connection string

**Required:** Yes

**Description:** Complete database connection URL

**Format:**

.. code-block:: text

   postgresql://[user]:[password]@[host]:[port]/[database][?options]

**Examples:**

.. code-block:: bash

   # Self-hosted
   DATABASE_URL=postgresql://construbot:password@postgres:5432/construbot

   # AWS RDS (with SSL)
   DATABASE_URL=postgresql://construbot:pwd@db.abc123.us-east-1.rds.amazonaws.com:5432/construbot?sslmode=require

   # With connection pooling options
   DATABASE_URL=postgresql://user:pwd@host:5432/db?sslmode=require&connect_timeout=10&options=-c%20statement_timeout=300000

**SSL modes:**

- ``disable`` - No SSL (not recommended for production)
- ``require`` - SSL required (recommended)
- ``verify-ca`` - Verify certificate authority
- ``verify-full`` - Full certificate verification

Cache and Queue
---------------

REDIS_URL
^^^^^^^^^

**Type:** Redis connection string

**Required:** Yes

**Description:** Redis for caching and Celery broker

**Format:**

.. code-block:: text

   redis://[:password]@[host]:[port]/[database]

**Examples:**

.. code-block:: bash

   # Self-hosted (no password)
   REDIS_URL=redis://redis:6379/0

   # With password
   REDIS_URL=redis://:mypassword@redis:6379/0

   # AWS ElastiCache
   REDIS_URL=redis://construbot.abc123.cache.amazonaws.com:6379/0

**Database numbers:**

- ``/0`` - Cache and sessions
- ``/1`` - Celery broker (optional separation)
- ``/2`` - Celery results (optional separation)

Security Settings
=================

SSL/HTTPS
---------

DJANGO_SECURE_SSL_REDIRECT
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Type:** Boolean

**Default:** False

**Description:** Redirect all HTTP requests to HTTPS

**Production value:**

.. code-block:: bash

   DJANGO_SECURE_SSL_REDIRECT=True

**Requires:**

- Valid SSL certificate
- HTTPS configured on web server/load balancer

DJANGO_SECURE_PROXY_SSL_HEADER
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Type:** Tuple (header name, header value)

**Default:** None

**Description:** Trust X-Forwarded-Proto header from proxy/load balancer

**Production value:**

.. code-block:: bash

   DJANGO_SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https

**When to use:**

- Behind nginx reverse proxy
- Behind AWS ALB/ELB
- Behind CloudFlare

HSTS (HTTP Strict Transport Security)
--------------------------------------

DJANGO_SECURE_HSTS_SECONDS
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Type:** Integer (seconds)

**Default:** 0 (disabled)

**Description:** Browser should only access via HTTPS for this many seconds

**Production value:**

.. code-block:: bash

   DJANGO_SECURE_HSTS_SECONDS=31536000  # 1 year

.. warning::
   **Test carefully before enabling!** Once set, browsers refuse HTTP connections.

DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Type:** Boolean

**Default:** False

**Description:** Apply HSTS to all subdomains

**Production value:**

.. code-block:: bash

   DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True

**Requires:** All subdomains support HTTPS

DJANGO_SECURE_HSTS_PRELOAD
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Type:** Boolean

**Default:** False

**Description:** Allow adding to browser HSTS preload lists

**Production value:**

.. code-block:: bash

   DJANGO_SECURE_HSTS_PRELOAD=True

**After enabling:**

Submit domain to https://hstspreload.org/

Cookie Security
---------------

DJANGO_SESSION_COOKIE_SECURE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Type:** Boolean

**Default:** False

**Description:** Only send session cookie over HTTPS

**Production value:**

.. code-block:: bash

   DJANGO_SESSION_COOKIE_SECURE=True

DJANGO_SESSION_COOKIE_HTTPONLY
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Type:** Boolean

**Default:** True

**Description:** Prevent JavaScript access to session cookie

**Production value:**

.. code-block:: bash

   DJANGO_SESSION_COOKIE_HTTPONLY=True

DJANGO_CSRF_COOKIE_SECURE
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Type:** Boolean

**Default:** False

**Description:** Only send CSRF cookie over HTTPS

**Production value:**

.. code-block:: bash

   DJANGO_CSRF_COOKIE_SECURE=True

DJANGO_CSRF_COOKIE_HTTPONLY
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Type:** Boolean

**Default:** False

**Description:** Prevent JavaScript access to CSRF cookie

**Production value:**

.. code-block:: bash

   DJANGO_CSRF_COOKIE_HTTPONLY=True

Content Security
----------------

DJANGO_SECURE_CONTENT_TYPE_NOSNIFF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Type:** Boolean

**Default:** False

**Description:** Prevent MIME type sniffing

**Production value:**

.. code-block:: bash

   DJANGO_SECURE_CONTENT_TYPE_NOSNIFF=True

DJANGO_SECURE_BROWSER_XSS_FILTER
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Type:** Boolean

**Default:** False

**Description:** Enable browser XSS filter

**Production value:**

.. code-block:: bash

   DJANGO_SECURE_BROWSER_XSS_FILTER=True

X_FRAME_OPTIONS
^^^^^^^^^^^^^^^

**Type:** String

**Default:** DENY

**Description:** Control iframe embedding

**Values:**

- ``DENY`` - Cannot be embedded (recommended)
- ``SAMEORIGIN`` - Can embed on same domain
- ``ALLOW-FROM https://example.com`` - Allow specific domain

**Production value:**

.. code-block:: bash

   X_FRAME_OPTIONS=DENY

Email Configuration
===================

DJANGO_EMAIL_BACKEND
^^^^^^^^^^^^^^^^^^^^

**Type:** String (Python import path)

**Required:** Yes

**Description:** Email backend to use

**Production values:**

.. code-block:: bash

   # Mailgun (recommended)
   DJANGO_EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend

   # SendGrid
   DJANGO_EMAIL_BACKEND=anymail.backends.sendgrid.EmailBackend

   # Amazon SES
   DJANGO_EMAIL_BACKEND=anymail.backends.amazon_ses.EmailBackend

   # SMTP (generic)
   DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

MAILGUN_API_KEY
^^^^^^^^^^^^^^^

**Type:** String

**Required:** If using Mailgun

**Description:** Mailgun API key

**Example:**

.. code-block:: bash

   MAILGUN_API_KEY=key-1234567890abcdef1234567890abcdef

**Get from:** https://app.mailgun.com/app/account/security/api_keys

MAILGUN_SENDER_DOMAIN
^^^^^^^^^^^^^^^^^^^^^

**Type:** String

**Required:** If using Mailgun

**Description:** Verified domain for sending

**Example:**

.. code-block:: bash

   MAILGUN_SENDER_DOMAIN=mg.example.com

DEFAULT_FROM_EMAIL
^^^^^^^^^^^^^^^^^^

**Type:** Email address

**Required:** Yes

**Description:** Default sender for emails

**Example:**

.. code-block:: bash

   DEFAULT_FROM_EMAIL=noreply@example.com

SERVER_EMAIL
^^^^^^^^^^^^

**Type:** Email address

**Default:** root@localhost

**Description:** Sender for error emails

**Example:**

.. code-block:: bash

   SERVER_EMAIL=errors@example.com

Static and Media Files
======================

USE_S3
^^^^^^

**Type:** Boolean

**Default:** False

**Description:** Use AWS S3 for media file storage

**Production value:**

.. code-block:: bash

   USE_S3=True

AWS_ACCESS_KEY_ID
^^^^^^^^^^^^^^^^^

**Type:** String

**Required:** If USE_S3=True

**Description:** AWS access key with S3 permissions

**Example:**

.. code-block:: bash

   AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE

AWS_SECRET_ACCESS_KEY
^^^^^^^^^^^^^^^^^^^^^^

**Type:** String

**Required:** If USE_S3=True

**Description:** AWS secret key

**Example:**

.. code-block:: bash

   AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

AWS_STORAGE_BUCKET_NAME
^^^^^^^^^^^^^^^^^^^^^^^^

**Type:** String

**Required:** If USE_S3=True

**Description:** S3 bucket name for media files

**Example:**

.. code-block:: bash

   AWS_STORAGE_BUCKET_NAME=construbot-media-example-com

AWS_S3_REGION_NAME
^^^^^^^^^^^^^^^^^^

**Type:** String

**Default:** us-east-1

**Description:** AWS region for S3 bucket

**Example:**

.. code-block:: bash

   AWS_S3_REGION_NAME=us-west-2

AWS_S3_CUSTOM_DOMAIN
^^^^^^^^^^^^^^^^^^^^

**Type:** String

**Default:** None (optional)

**Description:** CloudFront or custom domain for media files

**Example:**

.. code-block:: bash

   AWS_S3_CUSTOM_DOMAIN=d111111abcdef8.cloudfront.net

Monitoring and Logging
======================

SENTRY_DSN
^^^^^^^^^^

**Type:** String (URL)

**Default:** None (optional)

**Description:** Sentry error tracking DSN

**Example:**

.. code-block:: bash

   SENTRY_DSN=https://abcdef1234567890@o123456.ingest.sentry.io/7654321

**Get from:** Sentry project settings

SENTRY_ENVIRONMENT
^^^^^^^^^^^^^^^^^^

**Type:** String

**Default:** production

**Description:** Environment name in Sentry

**Examples:**

.. code-block:: bash

   SENTRY_ENVIRONMENT=production
   SENTRY_ENVIRONMENT=staging

SENTRY_SAMPLE_RATE
^^^^^^^^^^^^^^^^^^

**Type:** Float (0.0 to 1.0)

**Default:** 1.0

**Description:** Percentage of errors to send to Sentry

**Example:**

.. code-block:: bash

   SENTRY_SAMPLE_RATE=1.0  # Send 100% of errors

LOG_LEVEL
^^^^^^^^^

**Type:** String

**Default:** INFO

**Description:** Minimum log level to record

**Values:**

- ``DEBUG`` - Detailed information (development only)
- ``INFO`` - General informational messages (production recommended)
- ``WARNING`` - Warning messages
- ``ERROR`` - Error messages only
- ``CRITICAL`` - Critical errors only

**Production value:**

.. code-block:: bash

   LOG_LEVEL=INFO

CORS Configuration
==================

CORS_ALLOWED_ORIGINS
^^^^^^^^^^^^^^^^^^^^

**Type:** Comma-separated string

**Default:** Empty

**Description:** Allowed origins for CORS requests

**Example:**

.. code-block:: bash

   CORS_ALLOWED_ORIGINS=https://app.example.com,https://mobile.example.com

**When needed:**

- API consumed by separate frontend
- Mobile app accessing API
- Different subdomain for frontend

CORS_ALLOW_ALL_ORIGINS
^^^^^^^^^^^^^^^^^^^^^^^

**Type:** Boolean

**Default:** False

**Description:** Allow CORS from any origin

.. danger::
   **Never use in production!** Security risk.

**Development only:**

.. code-block:: bash

   CORS_ALLOW_ALL_ORIGINS=True

Celery Configuration
====================

CELERY_BROKER_URL
^^^^^^^^^^^^^^^^^

**Type:** Redis connection string

**Default:** Uses REDIS_URL

**Description:** Celery message broker

**Example:**

.. code-block:: bash

   CELERY_BROKER_URL=redis://redis:6379/1

**Usually same as REDIS_URL** but can use different database number.

CELERY_RESULT_BACKEND
^^^^^^^^^^^^^^^^^^^^^^

**Type:** Redis connection string

**Default:** Uses REDIS_URL

**Description:** Celery result storage

**Example:**

.. code-block:: bash

   CELERY_RESULT_BACKEND=redis://redis:6379/2

Optional Variables
==================

Library Mode
------------

CONSTRUBOT_AS_LIBRARY
^^^^^^^^^^^^^^^^^^^^^^

**Type:** Boolean

**Default:** False

**Description:** Run Construbot as Django app (not standalone)

**Example:**

.. code-block:: bash

   CONSTRUBOT_AS_LIBRARY=True

**Effects:**

- Disables admin interface
- Disables account management URLs
- Disables standalone authentication
- Allows embedding in existing Django project

See :doc:`../library-mode` for details.

Database Connection Pooling
----------------------------

DATABASE_CONN_MAX_AGE
^^^^^^^^^^^^^^^^^^^^^^

**Type:** Integer (seconds)

**Default:** 0 (new connection per request)

**Description:** How long to reuse database connections

**Production value:**

.. code-block:: bash

   DATABASE_CONN_MAX_AGE=600  # 10 minutes

**Benefits:**

- Reduced database connection overhead
- Better performance under load
- Lower database resource usage

Session Storage
---------------

SESSION_ENGINE
^^^^^^^^^^^^^^

**Type:** String

**Default:** django.contrib.sessions.backends.db

**Description:** Where to store sessions

**Options:**

.. code-block:: bash

   # Database (default)
   SESSION_ENGINE=django.contrib.sessions.backends.db

   # Cache (Redis) - faster
   SESSION_ENGINE=django.contrib.sessions.backends.cache

   # Cached database - best of both
   SESSION_ENGINE=django.contrib.sessions.backends.cached_db

**Production recommendation:**

.. code-block:: bash

   SESSION_ENGINE=django.contrib.sessions.backends.cached_db

Complete Production Example
============================

Minimal Production .env
-----------------------

.. code-block:: bash

   # Django Core
   DJANGO_SETTINGS_MODULE=construbot.config.settings.production
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=<generate-strong-50+-char-key>
   DJANGO_ALLOWED_HOSTS=example.com,www.example.com

   # Database
   DATABASE_URL=postgresql://user:pass@db.example.rds.amazonaws.com:5432/construbot?sslmode=require

   # Cache/Queue
   REDIS_URL=redis://:password@redis.example.cache.amazonaws.com:6379/0

   # Email
   DJANGO_EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend
   MAILGUN_API_KEY=key-xxxxxxxxxx
   MAILGUN_SENDER_DOMAIN=mg.example.com
   DEFAULT_FROM_EMAIL=noreply@example.com

   # Storage
   USE_S3=True
   AWS_ACCESS_KEY_ID=AKIAXXXXXX
   AWS_SECRET_ACCESS_KEY=xxxxxxxxxx
   AWS_STORAGE_BUCKET_NAME=construbot-media-example
   AWS_S3_REGION_NAME=us-east-1

   # Security
   DJANGO_SECURE_SSL_REDIRECT=True
   DJANGO_SECURE_HSTS_SECONDS=31536000
   DJANGO_SESSION_COOKIE_SECURE=True
   DJANGO_CSRF_COOKIE_SECURE=True

   # Monitoring
   SENTRY_DSN=https://xxx@sentry.io/xxx

Comprehensive Production .env
------------------------------

.. code-block:: bash

   # Django Core
   DJANGO_SETTINGS_MODULE=construbot.config.settings.production
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=<generate-strong-50+-char-key>
   DJANGO_ALLOWED_HOSTS=example.com,www.example.com,api.example.com
   DJANGO_READ_DOT_ENV_FILE=True

   # Database
   DATABASE_URL=postgresql://user:pass@db.example.rds.amazonaws.com:5432/construbot?sslmode=require&connect_timeout=10
   DATABASE_CONN_MAX_AGE=600

   # Cache/Queue
   REDIS_URL=redis://:password@redis.example.cache.amazonaws.com:6379/0
   CELERY_BROKER_URL=redis://:password@redis.example.cache.amazonaws.com:6379/1
   CELERY_RESULT_BACKEND=redis://:password@redis.example.cache.amazonaws.com:6379/2

   # Sessions
   SESSION_ENGINE=django.contrib.sessions.backends.cached_db

   # Email
   DJANGO_EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend
   MAILGUN_API_KEY=key-xxxxxxxxxx
   MAILGUN_SENDER_DOMAIN=mg.example.com
   DEFAULT_FROM_EMAIL=noreply@example.com
   SERVER_EMAIL=errors@example.com

   # Storage
   USE_S3=True
   AWS_ACCESS_KEY_ID=AKIAXXXXXX
   AWS_SECRET_ACCESS_KEY=xxxxxxxxxx
   AWS_STORAGE_BUCKET_NAME=construbot-media-example
   AWS_S3_REGION_NAME=us-west-2
   AWS_S3_CUSTOM_DOMAIN=d111111abcdef8.cloudfront.net

   # Security - SSL
   DJANGO_SECURE_SSL_REDIRECT=True
   DJANGO_SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https

   # Security - HSTS
   DJANGO_SECURE_HSTS_SECONDS=31536000
   DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
   DJANGO_SECURE_HSTS_PRELOAD=True

   # Security - Cookies
   DJANGO_SESSION_COOKIE_SECURE=True
   DJANGO_SESSION_COOKIE_HTTPONLY=True
   DJANGO_CSRF_COOKIE_SECURE=True
   DJANGO_CSRF_COOKIE_HTTPONLY=True

   # Security - Content
   DJANGO_SECURE_CONTENT_TYPE_NOSNIFF=True
   DJANGO_SECURE_BROWSER_XSS_FILTER=True
   X_FRAME_OPTIONS=DENY

   # Monitoring
   SENTRY_DSN=https://xxx@sentry.io/xxx
   SENTRY_ENVIRONMENT=production
   SENTRY_SAMPLE_RATE=1.0
   LOG_LEVEL=INFO

   # CORS (if needed)
   CORS_ALLOWED_ORIGINS=https://app.example.com

Validation
==========

Check Required Variables
-------------------------

.. code-block:: bash

   # Run Django checks
   docker compose run --rm django python manage.py check --deploy

**No warnings should appear.**

Test Configuration
------------------

.. code-block:: bash

   # Django shell
   docker compose run --rm django python manage.py shell

.. code-block:: python

   from django.conf import settings

   # Verify critical settings
   assert settings.DEBUG is False, "DEBUG must be False!"
   assert settings.SECRET_KEY != 'insecure-key', "Change SECRET_KEY!"
   assert len(settings.ALLOWED_HOSTS) > 0, "Set ALLOWED_HOSTS!"

   print(f"Database: {settings.DATABASES['default']['NAME']}")
   print(f"Redis: {settings.CACHES['default']['LOCATION']}")
   print(f"Email: {settings.EMAIL_BACKEND}")
   print(f"Static: {settings.STATIC_URL}")
   print(f"Media: {settings.MEDIA_URL}")

See Also
========

- :doc:`production-checklist` - Complete deployment checklist
- :doc:`../installation/configuration` - Development configuration
- :doc:`aws-ec2` - AWS deployment guide
- :doc:`static-media-files` - File storage configuration
- `Django Settings Reference <https://docs.djangoproject.com/en/3.2/ref/settings/>`_
