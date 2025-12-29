============================
Docker Compose for Production
============================

Production Docker Compose configuration for deploying Construbot.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

Construbot includes Docker Compose configurations for both development and production:

- ``docker-compose.yml`` - Default configuration (can be used for production)
- ``compose/production/`` - Production-specific Dockerfiles

This guide covers deploying Construbot using Docker Compose on a single server or multiple servers.

Production Architecture
=======================

Single Server Setup
-------------------

.. code-block:: text

   Docker Host (EC2/VPS)
   ├── nginx (reverse proxy + static files)
   ├── django (Gunicorn + Django app)
   ├── postgres (database)
   ├── redis (cache + Celery broker)
   └── celeryworker (background tasks)

**Suitable for:** <1000 users, small deployments

Multi-Server Setup
------------------

.. code-block:: text

   Server 1 (Application)
   ├── nginx
   ├── django (multiple instances)
   └── celeryworker

   Server 2 (Database)
   └── postgres (or use AWS RDS)

   Server 3 (Cache/Queue)
   └── redis (or use AWS ElastiCache)

**Suitable for:** >1000 users, high availability needs

Docker Compose Configuration
=============================

Production docker-compose.yml
------------------------------

The included ``docker-compose.yml`` can be used for production with proper environment configuration:

**Key services:**

.. code-block:: yaml

   version: '3'

   services:
     postgres:
       image: postgres:12-alpine
       volumes:
         - postgres_data:/var/lib/postgresql/data
       environment:
         - POSTGRES_DB=construbot
         - POSTGRES_USER=${POSTGRES_USER}
         - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

     redis:
       image: redis:6-alpine

     django:
       build:
         context: .
         dockerfile: ./compose/production/django/Dockerfile
       command: /start
       volumes:
         - static_volume:/app/staticfiles
         - media_volume:/app/media
       depends_on:
         - postgres
         - redis
       env_file:
         - ./.env

     nginx:
       build:
         context: .
         dockerfile: ./compose/production/nginx/Dockerfile
       volumes:
         - static_volume:/app/staticfiles:ro
         - media_volume:/app/media:ro
       ports:
         - "80:80"
         - "443:443"
       depends_on:
         - django

     celeryworker:
       build:
         context: .
         dockerfile: ./compose/production/django/Dockerfile
       command: /start-celeryworker
       depends_on:
         - redis
         - postgres
       env_file:
         - ./.env

   volumes:
     postgres_data:
     static_volume:
     media_volume:

Environment Configuration
=========================

Production .env File
--------------------

Create ``.env`` with production settings:

.. code-block:: bash

   # Django
   DJANGO_SETTINGS_MODULE=construbot.config.settings.production
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=<generate-strong-key>
   DJANGO_ALLOWED_HOSTS=example.com,www.example.com

   # Database
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   POSTGRES_DB=construbot
   POSTGRES_USER=construbot_prod
   POSTGRES_PASSWORD=<strong-password>
   DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

   # Redis
   REDIS_URL=redis://redis:6379/0

   # Email (example with Mailgun)
   DJANGO_EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend
   MAILGUN_API_KEY=<your-key>
   MAILGUN_SENDER_DOMAIN=mg.example.com
   DEFAULT_FROM_EMAIL=noreply@example.com

   # Security
   DJANGO_SECURE_SSL_REDIRECT=True
   DJANGO_SECURE_HSTS_SECONDS=31536000
   DJANGO_SESSION_COOKIE_SECURE=True
   DJANGO_CSRF_COOKIE_SECURE=True

   # Static/Media (local storage or S3)
   USE_S3=False  # Set to True for S3

   # Monitoring
   SENTRY_DSN=<your-sentry-dsn>
   SENTRY_ENVIRONMENT=production

Building for Production
========================

Initial Build
-------------

.. code-block:: bash

   # Set production environment
   make buildprod

   # Or manually:
   export DJANGO_SETTINGS_MODULE=construbot.config.settings.production
   export DJANGO_DEBUG=False
   docker-compose build

   # Start services
   docker-compose up -d

**What happens:**

1. Builds production Docker images
2. Starts all services in detached mode
3. Creates volumes for persistent data

Database Setup
--------------

.. code-block:: bash

   # Run migrations
   docker-compose run --rm django python manage.py migrate

   # Create superuser
   docker-compose run --rm django python manage.py createsuperuser

   # Collect static files
   docker-compose run --rm django python manage.py collectstatic --no-input

Nginx Configuration
===================

Production Nginx Setup
----------------------

Create ``compose/production/nginx/nginx.conf``:

.. code-block:: nginx

   upstream django {
       server django:8000;
   }

   server {
       listen 80;
       server_name example.com www.example.com;

       # Redirect to HTTPS
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl http2;
       server_name example.com www.example.com;

       # SSL Configuration
       ssl_certificate /etc/nginx/ssl/fullchain.pem;
       ssl_certificate_key /etc/nginx/ssl/privkey.pem;

       # SSL Settings
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers HIGH:!aNULL:!MD5;
       ssl_prefer_server_ciphers on;

       # Security Headers
       add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
       add_header X-Frame-Options "DENY" always;
       add_header X-Content-Type-Options "nosniff" always;

       # Static files
       location /static/ {
           alias /app/staticfiles/;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }

       # Media files
       location /media/ {
           alias /app/media/;
           expires 1y;
           add_header Cache-Control "public";
       }

       # Django application
       location / {
           proxy_pass http://django;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;

           # Timeouts
           proxy_connect_timeout 60s;
           proxy_send_timeout 60s;
           proxy_read_timeout 60s;
       }

       # Max upload size
       client_max_body_size 10M;
   }

SSL Certificate
---------------

**Using Let's Encrypt:**

.. code-block:: bash

   # Install certbot
   sudo apt install certbot python3-certbot-nginx

   # Obtain certificate
   sudo certbot --nginx -d example.com -d www.example.com

   # Auto-renewal (already configured with certbot)
   sudo certbot renew --dry-run

**Mount certificates in docker-compose.yml:**

.. code-block:: yaml

   nginx:
     volumes:
       - /etc/letsencrypt:/etc/nginx/ssl:ro

Gunicorn Configuration
======================

Production Gunicorn Settings
-----------------------------

Create ``compose/production/django/gunicorn_config.py``:

.. code-block:: python

   import multiprocessing

   # Bind
   bind = "0.0.0.0:8000"

   # Workers
   workers = multiprocessing.cpu_count() * 2 + 1
   worker_class = "sync"
   worker_connections = 1000

   # Timeouts
   timeout = 60
   graceful_timeout = 30
   keepalive = 2

   # Logging
   accesslog = "-"
   errorlog = "-"
   loglevel = "info"

   # Process naming
   proc_name = "construbot"

**Start command** in ``compose/production/django/start``:

.. code-block:: bash

   #!/bin/bash
   set -o errexit
   set -o pipefail
   set -o nounset

   python manage.py collectstatic --noinput
   gunicorn construbot.config.wsgi:application -c /gunicorn_config.py

Managing Services
=================

Starting and Stopping
---------------------

.. code-block:: bash

   # Start all services
   docker-compose up -d

   # Start specific service
   docker-compose up -d django

   # Stop all services
   docker-compose down

   # Stop without removing containers
   docker-compose stop

Viewing Logs
------------

.. code-block:: bash

   # All services
   docker-compose logs

   # Specific service
   docker-compose logs django

   # Follow logs
   docker-compose logs -f django

   # Last 100 lines
   docker-compose logs --tail=100 django

Restarting Services
-------------------

.. code-block:: bash

   # Restart all
   docker-compose restart

   # Restart specific service
   docker-compose restart django

   # Restart after code changes
   docker-compose restart django celeryworker

Scaling Services
----------------

.. code-block:: bash

   # Run multiple Django instances
   docker-compose up -d --scale django=3

   # Run multiple Celery workers
   docker-compose up -d --scale celeryworker=2

Updating Application
====================

Deployment Process
------------------

.. code-block:: bash

   # 1. Pull latest code
   git pull origin main

   # 2. Rebuild images
   docker-compose build django celeryworker

   # 3. Run migrations
   docker-compose run --rm django python manage.py migrate

   # 4. Collect static files
   docker-compose run --rm django python manage.py collectstatic --no-input

   # 5. Restart services
   docker-compose restart django celeryworker

   # 6. Verify
   docker-compose ps
   docker-compose logs django

Zero-Downtime Deployment
--------------------------

.. code-block:: bash

   # 1. Build new images
   docker-compose build django

   # 2. Run migrations (if any)
   docker-compose run --rm django python manage.py migrate

   # 3. Start new container alongside old
   docker-compose up -d --scale django=2 --no-recreate

   # 4. Wait for new container to be healthy
   sleep 10

   # 5. Stop old container
   docker-compose stop django

   # 6. Scale back to 1
   docker-compose up -d --scale django=1

Data Management
===============

Database Backups
----------------

**Automated backup script:**

.. code-block:: bash

   #!/bin/bash
   # /opt/construbot/scripts/backup.sh

   BACKUP_DIR="/backups/construbot"
   DATE=$(date +%Y%m%d_%H%M%S)

   # Create backup directory
   mkdir -p "$BACKUP_DIR"

   # Backup database
   docker-compose exec -T postgres pg_dump -U construbot construbot | \
     gzip > "$BACKUP_DIR/db_backup_$DATE.sql.gz"

   # Keep only last 7 days
   find "$BACKUP_DIR" -name "db_backup_*.sql.gz" -mtime +7 -delete

**Schedule with cron:**

.. code-block:: bash

   # crontab -e
   0 2 * * * /opt/construbot/scripts/backup.sh

Restore Database
----------------

.. code-block:: bash

   # Stop application
   docker-compose stop django celeryworker

   # Restore from backup
   gunzip -c backup.sql.gz | \
     docker-compose exec -T postgres psql -U construbot construbot

   # Restart application
   docker-compose start django celeryworker

Volume Management
-----------------

**List volumes:**

.. code-block:: bash

   docker volume ls

**Backup volume:**

.. code-block:: bash

   # Backup media files
   docker run --rm -v construbot_media_volume:/data \
     -v $(pwd)/backups:/backup \
     alpine tar czf /backup/media_backup.tar.gz /data

**Restore volume:**

.. code-block:: bash

   docker run --rm -v construbot_media_volume:/data \
     -v $(pwd)/backups:/backup \
     alpine tar xzf /backup/media_backup.tar.gz -C /

Monitoring
==========

Health Checks
-------------

Add health checks to ``docker-compose.yml``:

.. code-block:: yaml

   django:
     healthcheck:
       test: ["CMD", "python", "manage.py", "check"]
       interval: 30s
       timeout: 10s
       retries: 3
       start_period: 40s

Resource Usage
--------------

.. code-block:: bash

   # Container stats
   docker stats

   # Specific container
   docker stats construbot_django_1

   # Disk usage
   docker system df

Logs
----

**Configure log rotation** in ``/etc/docker/daemon.json``:

.. code-block:: json

   {
     "log-driver": "json-file",
     "log-opts": {
       "max-size": "10m",
       "max-file": "3"
     }
   }

Troubleshooting
===============

Container Won't Start
---------------------

.. code-block:: bash

   # Check logs
   docker-compose logs django

   # Check container status
   docker-compose ps

   # Inspect container
   docker inspect construbot_django_1

Database Connection Issues
--------------------------

.. code-block:: bash

   # Test database connection
   docker-compose exec django python manage.py dbshell

   # Check database logs
   docker-compose logs postgres

   # Verify DATABASE_URL
   docker-compose exec django env | grep DATABASE_URL

Out of Disk Space
-----------------

.. code-block:: bash

   # Check disk usage
   df -h
   docker system df

   # Clean up unused resources
   docker system prune -a

   # Remove old volumes
   docker volume prune

Performance Issues
------------------

.. code-block:: bash

   # Check resource usage
   docker stats

   # Scale up workers
   docker-compose up -d --scale django=2 --scale celeryworker=2

   # Increase Gunicorn workers in gunicorn_config.py

See Also
========

- :doc:`production-checklist` - Pre-deployment checklist
- :doc:`aws-ec2` - AWS EC2 deployment guide
- :doc:`environment-variables` - Environment configuration
- :doc:`../architecture/overview` - Application architecture
