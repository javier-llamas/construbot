=====================
Production Checklist
=====================

Complete pre-deployment checklist to ensure your Construbot installation is production-ready.

.. contents:: Table of Contents
   :local:
   :depth: 2

.. danger::
   **DO NOT deploy to production without completing this checklist!** Skipping items can lead to security vulnerabilities, data loss, or application downtime.

Overview
========

This checklist covers all critical configuration items for production deployment. Work through each section systematically and verify each item before going live.

**Estimated time:** 2-4 hours for first deployment

Critical Settings
=================

DEBUG Mode
----------

.. code-block:: bash

   ✓ Set DEBUG=False in production

**Verify:**

.. code-block:: bash

   # In .env
   DJANGO_DEBUG=False

.. danger::
   **Never run production with DEBUG=True!** This exposes:

   - Full tracebacks with code
   - SQL queries and database schema
   - Environment variables and secrets
   - Internal file paths

**Test:**

.. code-block:: python

   # In Django shell
   from django.conf import settings
   assert settings.DEBUG is False, "DEBUG must be False in production!"

SECRET_KEY
----------

.. code-block:: bash

   ✓ Generate unique, strong SECRET_KEY
   ✓ Never use development SECRET_KEY in production
   ✓ Store SECRET_KEY securely (not in version control)

**Generate:**

.. code-block:: bash

   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

**Set in .env:**

.. code-block:: bash

   DJANGO_SECRET_KEY=<generated-key-here>

**Verify:**

.. code-block:: bash

   # Key should be 50+ characters, random
   echo $DJANGO_SECRET_KEY | wc -c

ALLOWED_HOSTS
-------------

.. code-block:: bash

   ✓ Configure ALLOWED_HOSTS with production domains
   ✓ Include all domains (www and root)
   ✓ Include load balancer hostname if applicable

**Set:**

.. code-block:: bash

   # Comma-separated list
   DJANGO_ALLOWED_HOSTS=example.com,www.example.com,construbot.example.com

**Test:**

.. code-block:: bash

   # Should work
   curl -H "Host: example.com" https://example.com

   # Should fail with 400 Bad Request
   curl -H "Host: malicious.com" https://example.com

Settings Module
---------------

.. code-block:: bash

   ✓ Set DJANGO_SETTINGS_MODULE=construbot.config.settings.production

**Verify:**

.. code-block:: bash

   echo $DJANGO_SETTINGS_MODULE
   # Should show: construbot.config.settings.production

Security Configuration
======================

HTTPS/SSL
---------

.. code-block:: bash

   ✓ Obtain SSL certificate (Let's Encrypt recommended)
   ✓ Configure web server for HTTPS
   ✓ Redirect HTTP to HTTPS
   ✓ Enable HSTS

**Environment variables:**

.. code-block:: bash

   DJANGO_SECURE_SSL_REDIRECT=True
   DJANGO_SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https

**HSTS (HTTP Strict Transport Security):**

.. code-block:: bash

   DJANGO_SECURE_HSTS_SECONDS=31536000  # 1 year
   DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
   DJANGO_SECURE_HSTS_PRELOAD=True

.. warning::
   **Test HSTS carefully!** Once enabled with preload, browsers will refuse non-HTTPS connections even if you disable it.

Cookie Security
---------------

.. code-block:: bash

   ✓ Enable secure cookies
   ✓ Enable HttpOnly cookies
   ✓ Configure CSRF protection

**Set:**

.. code-block:: bash

   DJANGO_SESSION_COOKIE_SECURE=True
   DJANGO_SESSION_COOKIE_HTTPONLY=True
   DJANGO_CSRF_COOKIE_SECURE=True
   DJANGO_CSRF_COOKIE_HTTPONLY=True

Content Security
----------------

.. code-block:: bash

   ✓ Enable content type sniffing protection
   ✓ Enable XSS filter
   ✓ Configure X-Frame-Options

**Set:**

.. code-block:: bash

   DJANGO_SECURE_CONTENT_TYPE_NOSNIFF=True
   DJANGO_SECURE_BROWSER_XSS_FILTER=True
   X_FRAME_OPTIONS=DENY

**Run Django security check:**

.. code-block:: bash

   python manage.py check --deploy

Expected output should have **no warnings**.

Database Configuration
======================

PostgreSQL Setup
----------------

.. code-block:: bash

   ✓ Use PostgreSQL (not SQLite)
   ✓ Configure production database credentials
   ✓ Enable SSL connection
   ✓ Set up connection pooling
   ✓ Configure automated backups

**DATABASE_URL:**

.. code-block:: bash

   # With SSL (recommended)
   DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require

   # AWS RDS example
   DATABASE_URL=postgresql://construbot:password@construbot.abc123.us-east-1.rds.amazonaws.com:5432/construbot?sslmode=require

**Verify connection:**

.. code-block:: bash

   docker-compose run --rm django python manage.py dbshell
   # Should connect without errors

Database Migrations
-------------------

.. code-block:: bash

   ✓ Run migrations on production database
   ✓ Verify all migrations applied
   ✓ Test rollback procedure

**Apply migrations:**

.. code-block:: bash

   docker-compose run --rm django python manage.py migrate

**Check status:**

.. code-block:: bash

   docker-compose run --rm django python manage.py showmigrations

All migrations should show ``[X]`` (applied).

Backup Strategy
---------------

.. code-block:: bash

   ✓ Configure automated database backups
   ✓ Test backup restoration
   ✓ Set backup retention policy (7-30 days)
   ✓ Store backups off-site (different region)

**AWS RDS:**

- Enable automated backups
- Set backup window (low-traffic time)
- Configure backup retention (7-35 days)
- Enable Multi-AZ for high availability

**Self-hosted:**

.. code-block:: bash

   # Set up daily backup cron job
   0 2 * * * /opt/construbot/scripts/backup.sh

Static and Media Files
======================

Static Files
------------

.. code-block:: bash

   ✓ Collect static files
   ✓ Configure WhiteNoise
   ✓ Set up CDN (optional but recommended)
   ✓ Enable compression

**Collect static files:**

.. code-block:: bash

   docker-compose run --rm django python manage.py collectstatic --no-input

**Verify:**

.. code-block:: bash

   ls staticfiles/
   # Should contain admin/, css/, js/, etc.

**WhiteNoise** is configured by default in ``construbot.config.settings.production``.

Media Files
-----------

.. code-block:: bash

   ✓ Configure media file storage (S3 recommended)
   ✓ Set up bucket with proper permissions
   ✓ Configure CORS if accessing from different domain
   ✓ Enable CDN for media files (optional)

**Using AWS S3:**

.. code-block:: bash

   USE_S3=True
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_STORAGE_BUCKET_NAME=construbot-media
   AWS_S3_REGION_NAME=us-east-1

**S3 Bucket Configuration:**

1. Create S3 bucket
2. Block public access (use signed URLs)
3. Configure CORS if needed
4. Set up lifecycle policies for old files

**Test upload:**

.. code-block:: bash

   # Upload test file through Django admin
   # Verify file appears in S3 bucket

Email Configuration
===================

Email Service
-------------

.. code-block:: bash

   ✓ Configure production email backend
   ✓ Set up email service (Mailgun, SendGrid, SES)
   ✓ Verify sender domain
   ✓ Configure SPF, DKIM, DMARC records

**Using Mailgun (recommended):**

.. code-block:: bash

   DJANGO_EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend
   MAILGUN_API_KEY=your-api-key
   MAILGUN_SENDER_DOMAIN=mg.example.com
   DEFAULT_FROM_EMAIL=noreply@example.com
   SERVER_EMAIL=errors@example.com

**Using Amazon SES:**

.. code-block:: bash

   DJANGO_EMAIL_BACKEND=anymail.backends.amazon_ses.EmailBackend
   AWS_ACCESS_KEY_ID=your-key
   AWS_SECRET_ACCESS_KEY=your-secret
   AWS_SES_REGION_NAME=us-east-1
   DEFAULT_FROM_EMAIL=noreply@example.com

Email Testing
-------------

.. code-block:: bash

   ✓ Send test email
   ✓ Verify delivery
   ✓ Check spam score
   ✓ Verify sender reputation

**Test:**

.. code-block:: bash

   docker-compose run --rm django python manage.py shell

.. code-block:: python

   from django.core.mail import send_mail
   send_mail(
       'Test Email',
       'This is a test from Construbot.',
       'noreply@example.com',
       ['your-email@example.com'],
   )

Check your inbox and spam folder.

Caching and Performance
=======================

Redis Configuration
-------------------

.. code-block:: bash

   ✓ Configure production Redis instance
   ✓ Enable password authentication
   ✓ Configure persistence (if needed)
   ✓ Set up Redis backups

**Using AWS ElastiCache:**

.. code-block:: bash

   REDIS_URL=redis://:password@your-redis-endpoint.cache.amazonaws.com:6379/0

**Self-hosted:**

.. code-block:: bash

   REDIS_URL=redis://:password@localhost:6379/0

**Test connection:**

.. code-block:: bash

   redis-cli -h your-redis-host -a your-password ping
   # Should respond: PONG

Celery Configuration
--------------------

.. code-block:: bash

   ✓ Configure Celery broker (Redis)
   ✓ Configure result backend
   ✓ Set up Celery worker as systemd service or Docker container
   ✓ Configure Celery beat for periodic tasks (if needed)

**Start Celery worker:**

.. code-block:: bash

   # Add to docker-compose.yml or run as separate service
   docker-compose up -d celeryworker

**Verify:**

.. code-block:: bash

   docker-compose logs celeryworker
   # Should show: "[INFO/MainProcess] Connected to redis://..."

Monitoring and Logging
=======================

Error Tracking
--------------

.. code-block:: bash

   ✓ Configure Sentry for error tracking
   ✓ Test error reporting
   ✓ Set up email alerts
   ✓ Configure error notifications

**Set up Sentry:**

.. code-block:: bash

   SENTRY_DSN=https://your-key@sentry.io/project-id
   SENTRY_ENVIRONMENT=production
   SENTRY_SAMPLE_RATE=1.0

**Test:**

.. code-block:: python

   # In Django shell
   from sentry_sdk import capture_message
   capture_message("Test error from production")

Check Sentry dashboard for the message.

Application Logging
-------------------

.. code-block:: bash

   ✓ Configure log level (INFO or WARNING for production)
   ✓ Set up log rotation
   ✓ Configure centralized logging (optional)

**Set log level:**

.. code-block:: bash

   LOG_LEVEL=INFO

**Log aggregation options:**

- CloudWatch Logs (AWS)
- Papertrail
- Loggly
- ELK Stack

Server Monitoring
-----------------

.. code-block:: bash

   ✓ Set up uptime monitoring
   ✓ Configure performance monitoring
   ✓ Set up disk space alerts
   ✓ Monitor database performance

**Uptime monitoring:**

- UptimeRobot (free)
- Pingdom
- StatusCake

**Performance monitoring:**

- New Relic
- DataDog
- Application Insights

**Server monitoring:**

- CloudWatch (AWS)
- DigitalOcean Monitoring
- Prometheus + Grafana

Infrastructure
==============

Server Configuration
--------------------

.. code-block:: bash

   ✓ Configure firewall (allow only 22, 80, 443)
   ✓ Set up SSH key authentication
   ✓ Disable root login
   ✓ Configure automatic security updates
   ✓ Set up fail2ban (brute force protection)

**Firewall (UFW):**

.. code-block:: bash

   sudo ufw allow 22/tcp   # SSH
   sudo ufw allow 80/tcp   # HTTP
   sudo ufw allow 443/tcp  # HTTPS
   sudo ufw enable

**SSH hardening:**

.. code-block:: bash

   # Edit /etc/ssh/sshd_config
   PermitRootLogin no
   PasswordAuthentication no
   PubkeyAuthentication yes

   # Restart SSH
   sudo systemctl restart sshd

DNS Configuration
-----------------

.. code-block:: bash

   ✓ Point domain to server IP
   ✓ Configure A record (root and www)
   ✓ Set up DNS propagation (may take 24-48 hours)
   ✓ Configure MX records for email (if needed)

**Example DNS records:**

.. code-block:: text

   Type    Name    Value                   TTL
   A       @       123.45.67.89            3600
   A       www     123.45.67.89            3600
   CNAME   api     example.com             3600

**Verify:**

.. code-block:: bash

   dig example.com
   dig www.example.com

Load Balancer (Optional)
-------------------------

.. code-block:: bash

   ✓ Configure load balancer (if using multiple servers)
   ✓ Set up health checks
   ✓ Configure SSL termination
   ✓ Enable sticky sessions

Application Testing
===================

Functionality Tests
-------------------

.. code-block:: bash

   ✓ Create test user account
   ✓ Log in to application
   ✓ Create test project/contract
   ✓ Generate PDF report
   ✓ Upload test image
   ✓ Send test email
   ✓ Test API endpoints (if using)

**Checklist:**

- [ ] Homepage loads
- [ ] User login works
- [ ] Dashboard displays correctly
- [ ] Create new client (Contraparte)
- [ ] Create new contract (Contrato)
- [ ] Add concepts (Conceptos) to contract
- [ ] Create estimate (Estimación)
- [ ] Generate PDF document
- [ ] Upload image to media library
- [ ] Receive email notification

Performance Testing
-------------------

.. code-block:: bash

   ✓ Test page load times (<2 seconds)
   ✓ Test concurrent users (use load testing tool)
   ✓ Verify database query performance
   ✓ Check static file loading speed

**Tools:**

.. code-block:: bash

   # Apache Bench (simple load test)
   ab -n 1000 -c 10 https://example.com/

   # Locust (advanced load testing)
   pip install locust
   # Create locustfile.py and run load tests

Security Testing
----------------

.. code-block:: bash

   ✓ Run Django security check
   ✓ Scan for common vulnerabilities
   ✓ Test SQL injection protection
   ✓ Test XSS protection
   ✓ Verify CSRF protection

**Django security check:**

.. code-block:: bash

   python manage.py check --deploy

**OWASP ZAP scan:**

.. code-block:: bash

   # Download OWASP ZAP
   # Run automated scan against your domain
   # Review and fix any critical/high vulnerabilities

Final Verification
==================

Pre-Launch Checklist
--------------------

**Critical (must be complete):**

- [ ] DEBUG=False
- [ ] Unique, strong SECRET_KEY
- [ ] ALLOWED_HOSTS configured
- [ ] Production database configured
- [ ] SSL certificate installed
- [ ] Static files collected
- [ ] Media storage configured
- [ ] Email service working
- [ ] Backups configured
- [ ] Error tracking (Sentry) configured

**Important (strongly recommended):**

- [ ] HSTS enabled
- [ ] Cookie security enabled
- [ ] Redis configured
- [ ] Celery worker running
- [ ] Monitoring set up
- [ ] Logs configured
- [ ] DNS configured
- [ ] Firewall configured

**Optional (nice to have):**

- [ ] CDN for static files
- [ ] CDN for media files
- [ ] Load balancer
- [ ] Multiple servers
- [ ] Read replicas

Launch Day
----------

.. code-block:: bash

   ✓ Schedule deployment during low-traffic period
   ✓ Announce maintenance window to users
   ✓ Have rollback plan ready
   ✓ Monitor errors closely for first 24 hours
   ✓ Be available for immediate fixes

**Deployment steps:**

1. Backup current database
2. Put application in maintenance mode
3. Pull latest code
4. Run migrations
5. Collect static files
6. Restart services
7. Verify functionality
8. Remove maintenance mode
9. Monitor logs and Sentry

Post-Launch Monitoring
-----------------------

**First 24 hours:**

- Monitor Sentry for errors every hour
- Check server resources (CPU, memory, disk)
- Verify email delivery
- Check application performance
- Review user feedback

**First week:**

- Daily error reviews
- Performance optimization based on real usage
- Database query optimization
- Adjust caching as needed

**Ongoing:**

- Weekly security updates
- Monthly dependency updates
- Quarterly disaster recovery drills
- Continuous monitoring and optimization

Troubleshooting Common Issues
==============================

Application Won't Start
-----------------------

**Check:**

1. Environment variables set correctly
2. Database accessible
3. Redis accessible
4. Migrations applied
5. No syntax errors in settings

**Debug:**

.. code-block:: bash

   docker-compose logs django
   # Look for Python tracebacks

502 Bad Gateway
---------------

**Causes:**

- Gunicorn not running
- Upstream server timeout
- Nginx misconfigured

**Fix:**

.. code-block:: bash

   # Restart services
   docker-compose restart django

   # Check Gunicorn logs
   docker-compose logs django

500 Internal Server Error
--------------------------

**Debug:**

1. Check Sentry for error details
2. Review Django logs
3. Test database connection
4. Verify all settings correct

.. code-block:: bash

   # Test in shell
   docker-compose run --rm django python manage.py shell

   from django.conf import settings
   print(settings.DATABASES)

Static Files Not Loading
-------------------------

**Fix:**

.. code-block:: bash

   # Recollect static files
   docker-compose run --rm django python manage.py collectstatic --clear --no-input

   # Verify STATIC_ROOT
   docker-compose run --rm django python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.STATIC_ROOT)

Documentation
=============

Required Documentation
----------------------

.. code-block:: bash

   ✓ Document server credentials (store securely)
   ✓ Document deployment process
   ✓ Create runbook for common operations
   ✓ Document rollback procedure
   ✓ Create disaster recovery plan

**Runbook should include:**

- How to deploy updates
- How to restart services
- How to restore from backup
- Common troubleshooting steps
- Emergency contacts

See Also
========

- :doc:`docker-compose` - Docker Compose production setup
- :doc:`aws-ec2` - AWS EC2 deployment guide
- :doc:`environment-variables` - Environment configuration reference
- :doc:`static-media-files` - Static and media file configuration
- `Django Deployment Checklist <https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/>`_
