==========
Deployment
==========

Production deployment guides for Construbot on various platforms and infrastructures.

Overview
========

This section covers deploying Construbot to production environments. Whether you're deploying to cloud infrastructure, on-premises servers, or Platform-as-a-Service (PaaS) providers, these guides will help you get Construbot running securely and efficiently.

.. warning::
   **Production deployment requires careful configuration.** Never use development settings in production. Always follow the security checklist before going live.

Deployment Options
==================

Construbot can be deployed using several approaches:

**Docker-based Deployment (Recommended)**

- Use Docker Compose for production orchestration
- Deploy to AWS EC2, DigitalOcean, or any VPS
- Consistent environment across dev and production
- Easy scaling and updates

**Platform-as-a-Service (PaaS)**

- Heroku, Railway, Render
- Managed database and infrastructure
- Simpler setup, less configuration
- Higher cost for equivalent resources

**Traditional Server Deployment**

- Install directly on Linux server
- More control over environment
- Requires system administration experience
- Manual dependency management

Quick Start (Docker + AWS EC2)
===============================

For the impatient, here's the minimal steps to deploy:

.. code-block:: bash

   # 1. Launch EC2 instance (Ubuntu 22.04, t2.small or larger)
   # 2. SSH into instance
   # 3. Install Docker and Docker Compose
   # 4. Clone repository
   git clone https://github.com/javier-llamas/construbot.git
   cd construbot

   # 5. Configure environment
   cp .env.example .env
   nano .env  # Set production variables

   # 6. Build and start
   make buildprod

   # 7. Create superuser
   docker-compose -f docker-compose.yml run --rm django python manage.py createsuperuser

   # 8. Assign Elastic IP and configure domain

**For detailed instructions, see:** :doc:`aws-ec2`

Prerequisites
=============

Before Deployment
-----------------

**Required:**

- Domain name (for HTTPS and production use)
- SSL certificate (Let's Encrypt recommended)
- Production database (PostgreSQL 12+)
- Email service (Mailgun, SendGrid, or SES)
- Basic Linux server administration knowledge

**Recommended:**

- Redis instance for caching
- S3 bucket for media files
- Monitoring service (Sentry)
- CDN for static files
- Backup strategy

**Security:**

- Firewall configuration
- SSH key-based authentication
- Non-root deployment user
- Regular security updates

Infrastructure Options
----------------------

**Compute:**

- AWS EC2 (t2.small minimum, t2.medium recommended)
- DigitalOcean Droplets ($12-24/month)
- Linode, Vultr, Hetzner
- Google Cloud Compute Engine
- Microsoft Azure VMs

**Database:**

- AWS RDS for PostgreSQL (recommended for production)
- Managed PostgreSQL (DigitalOcean, Heroku Postgres)
- Self-hosted PostgreSQL on VPS
- Minimum: db.t3.micro (AWS RDS)

**Storage:**

- AWS S3 for media files (recommended)
- DigitalOcean Spaces
- Google Cloud Storage
- Azure Blob Storage
- Local storage (only for small deployments)

Deployment Guides
=================

.. toctree::
   :maxdepth: 2

   production-checklist
   docker-compose
   aws-ec2
   static-media-files
   environment-variables

Step-by-Step Process
=====================

1. Pre-Deployment
-----------------

**Review checklist:**

.. code-block:: bash

   # See comprehensive checklist
   See: :doc:`production-checklist`

**Key items:**

- [ ] Set ``DEBUG=False``
- [ ] Configure ``SECRET_KEY`` (unique, strong)
- [ ] Set ``ALLOWED_HOSTS``
- [ ] Configure production database
- [ ] Set up email service
- [ ] Configure static/media file storage
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring (Sentry)

2. Infrastructure Setup
-----------------------

**Create server instance:**

- Choose cloud provider (AWS, DigitalOcean, etc.)
- Select Ubuntu 22.04 LTS
- Minimum: 2 CPU, 4 GB RAM
- Attach storage volume for database (if self-hosting)

**Configure domain:**

- Point A record to server IP
- Configure DNS (www and root domain)
- Set up SSL certificate (Let's Encrypt)

3. Server Preparation
---------------------

**Install dependencies:**

.. code-block:: bash

   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh

   # Install Docker Compose
   sudo apt install docker-compose-plugin

   # Configure firewall
   sudo ufw allow 22    # SSH
   sudo ufw allow 80    # HTTP
   sudo ufw allow 443   # HTTPS
   sudo ufw enable

**Create deployment user:**

.. code-block:: bash

   # Create user
   sudo adduser construbot
   sudo usermod -aG docker construbot
   sudo usermod -aG sudo construbot

   # Switch to deployment user
   su - construbot

4. Application Deployment
--------------------------

**Clone and configure:**

.. code-block:: bash

   # Clone repository
   git clone https://github.com/javier-llamas/construbot.git
   cd construbot

   # Configure environment
   cp .env.example .env
   nano .env  # Set all production variables

   # See: environment-variables for complete reference

**Build and run:**

.. code-block:: bash

   # Build production images
   make buildprod

   # Run migrations
   docker-compose run --rm django python manage.py migrate

   # Create superuser
   docker-compose run --rm django python manage.py createsuperuser

   # Collect static files
   docker-compose run --rm django python manage.py collectstatic --no-input

**Start services:**

.. code-block:: bash

   # Start in background
   docker-compose up -d

   # Check status
   docker-compose ps

   # View logs
   docker-compose logs -f

5. Post-Deployment
------------------

**Verify functionality:**

- [ ] Access application via domain
- [ ] Test user login
- [ ] Create test project/contract
- [ ] Generate PDF report
- [ ] Send test email
- [ ] Check static files loading
- [ ] Upload test image (media files)

**Set up monitoring:**

.. code-block:: bash

   # Configure Sentry (in .env)
   SENTRY_DSN=your-dsn

   # Set up application monitoring
   # - Uptime monitoring (UptimeRobot, Pingdom)
   # - Log aggregation (CloudWatch, Papertrail)
   # - Performance monitoring (New Relic, DataDog)

**Configure backups:**

.. code-block:: bash

   # Database backup script
   # See: backup-and-restore section below

Production Architecture
=======================

Recommended Setup
-----------------

.. code-block:: text

   ┌─────────────────────────────────────────────┐
   │              Internet                        │
   └─────────────┬───────────────────────────────┘
                 │
                 ▼
   ┌─────────────────────────────────────────────┐
   │     CDN (CloudFront / CloudFlare)           │
   │          (Static Files)                      │
   └─────────────────────────────────────────────┘
                 │
                 ▼
   ┌─────────────────────────────────────────────┐
   │   Load Balancer (ALB / Nginx)               │
   │         (HTTPS Termination)                  │
   └─────────────┬───────────────────────────────┘
                 │
                 ▼
   ┌─────────────────────────────────────────────┐
   │        Web Servers (EC2 / Droplets)         │
   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
   │  │ Django 1 │  │ Django 2 │  │ Django N │  │
   │  │ + Nginx  │  │ + Nginx  │  │ + Nginx  │  │
   │  └──────────┘  └──────────┘  └──────────┘  │
   └────┬────────────────┬───────────────────────┘
        │                │
        ▼                ▼
   ┌─────────┐    ┌──────────────┐
   │   RDS   │    │    Redis     │
   │(PostgreSQL)  │ (ElastiCache)│
   └─────────┘    └──────────────┘
        │
        ▼
   ┌─────────────────┐
   │       S3        │
   │  (Media Files)  │
   └─────────────────┘

**Components:**

- **CDN:** Serve static files globally with low latency
- **Load Balancer:** Distribute traffic, HTTPS termination, health checks
- **Web Servers:** Django application + Gunicorn + Nginx
- **Database:** Managed PostgreSQL (RDS) with automated backups
- **Cache:** Redis for caching and Celery broker
- **Storage:** S3 for user-uploaded media files

Single Server Setup
--------------------

For smaller deployments:

.. code-block:: text

   ┌─────────────────────────────────────────────┐
   │         Single EC2 Instance                 │
   │  ┌──────────────────────────────────────┐   │
   │  │  Docker Compose Services:            │   │
   │  │  ┌────────┐  ┌──────────┐            │   │
   │  │  │ Nginx  │  │  Django  │            │   │
   │  │  │ (proxy)│  │(Gunicorn)│            │   │
   │  │  └────────┘  └──────────┘            │   │
   │  │  ┌──────────┐  ┌──────────┐          │   │
   │  │  │Postgres  │  │  Redis   │          │   │
   │  │  │(database)│  │ (cache)  │          │   │
   │  │  └──────────┘  └──────────┘          │   │
   │  │  ┌──────────┐                        │   │
   │  │  │  Celery  │                        │   │
   │  │  │ (worker) │                        │   │
   │  │  └──────────┘                        │   │
   │  └──────────────────────────────────────┘   │
   └─────────────────────────────────────────────┘
             │
             ▼
      ┌────────────┐
      │     S3     │
      │(Media Files)│
      └────────────┘

**Suitable for:**

- <1000 daily active users
- Development/staging environments
- Small construction companies
- Budget-constrained deployments

Backup and Restore
==================

Database Backups
----------------

**Automated backups (AWS RDS):**

RDS automatically creates daily snapshots. Configure:

- Retention period (7-35 days)
- Backup window (low-traffic hours)
- Multi-AZ for high availability

**Manual backups (self-hosted):**

.. code-block:: bash

   # Backup script
   #!/bin/bash
   BACKUP_DIR="/backups/construbot"
   DATE=$(date +%Y%m%d_%H%M%S)

   # Dump database
   docker-compose exec -T postgres pg_dump -U construbot construbot > \
     "$BACKUP_DIR/db_backup_$DATE.sql"

   # Compress
   gzip "$BACKUP_DIR/db_backup_$DATE.sql"

   # Upload to S3
   aws s3 cp "$BACKUP_DIR/db_backup_$DATE.sql.gz" \
     s3://construbot-backups/database/

**Automate with cron:**

.. code-block:: bash

   # Add to crontab: crontab -e
   0 2 * * * /opt/construbot/scripts/backup.sh

Media File Backups
------------------

**If using S3:**

- Enable S3 versioning
- Configure lifecycle policies
- Cross-region replication (optional)

**If using local storage:**

.. code-block:: bash

   # Sync media files to S3
   aws s3 sync /path/to/media/ s3://construbot-backups/media/

Restore Process
---------------

**Database restore:**

.. code-block:: bash

   # Stop application
   docker-compose down

   # Restore from backup
   gunzip -c db_backup_20240101_020000.sql.gz | \
     docker-compose exec -T postgres psql -U construbot construbot

   # Start application
   docker-compose up -d

**Media restore:**

.. code-block:: bash

   # From S3
   aws s3 sync s3://construbot-backups/media/ /path/to/media/

Scaling Considerations
======================

Vertical Scaling
----------------

**When to scale up:**

- High CPU usage (>70% sustained)
- Memory pressure
- Slow database queries
- Single server bottleneck

**How to scale:**

- Increase instance size (t2.small → t2.medium → t2.large)
- Add more CPU/RAM
- Upgrade database instance
- Use faster storage (SSD)

Horizontal Scaling
------------------

**When to scale out:**

- >1000 concurrent users
- Geographic distribution needed
- High availability requirements
- Load balancing benefits

**How to scale:**

- Add more application servers
- Set up load balancer
- Use managed database (RDS)
- External Redis (ElastiCache)
- CDN for static files

Performance Optimization
------------------------

**Database:**

- Connection pooling
- Query optimization
- Read replicas
- Database indexes

**Caching:**

- Redis for session storage
- Template fragment caching
- Database query caching
- Full-page caching (Varnish)

**Static Files:**

- CDN distribution
- Gzip compression
- Browser caching headers
- Image optimization

Security Hardening
==================

Essential Security Measures
----------------------------

**Application security:**

.. code-block:: bash

   # Run Django security checks
   python manage.py check --deploy

**Server security:**

.. code-block:: bash

   # Automatic security updates
   sudo apt install unattended-upgrades
   sudo dpkg-reconfigure --priority=low unattended-upgrades

   # Fail2ban (brute force protection)
   sudo apt install fail2ban

   # SSH hardening
   # Edit /etc/ssh/sshd_config:
   # - Disable root login
   # - Disable password authentication
   # - Change default port

**SSL/TLS:**

- Use Let's Encrypt for free certificates
- Enable HSTS
- Configure secure ciphers
- Set up certificate auto-renewal

**Environment secrets:**

- Never commit secrets to git
- Use environment variables
- Rotate credentials regularly
- Use secrets management (AWS Secrets Manager)

Monitoring and Logging
=======================

Application Monitoring
----------------------

**Sentry (Error Tracking):**

.. code-block:: bash

   # In .env
   SENTRY_DSN=https://...@sentry.io/...
   SENTRY_ENVIRONMENT=production

**Application Performance Monitoring:**

- New Relic
- DataDog
- Application Insights

Server Monitoring
-----------------

**Metrics to monitor:**

- CPU usage
- Memory usage
- Disk space
- Network traffic
- Database connections
- Response times

**Tools:**

- CloudWatch (AWS)
- Prometheus + Grafana
- DigitalOcean Monitoring
- Netdata

Log Aggregation
---------------

**Centralized logging:**

- CloudWatch Logs (AWS)
- Papertrail
- Loggly
- ELK Stack (Elasticsearch, Logstash, Kibana)

**Log rotation:**

.. code-block:: bash

   # Configure logrotate for application logs
   # /etc/logrotate.d/construbot

Troubleshooting
===============

Common Issues
-------------

**Application won't start:**

.. code-block:: bash

   # Check logs
   docker-compose logs django

   # Common causes:
   # - Missing environment variables
   # - Database connection failed
   # - Migration errors

**502 Bad Gateway:**

- Django not running
- Gunicorn crashed
- Nginx misconfigured

**500 Internal Server Error:**

- Check Sentry
- Review Django logs
- Verify database connection

**Static files not loading:**

- Run collectstatic
- Check STATIC_ROOT/STATIC_URL
- Verify WhiteNoise configuration
- Check CDN configuration

**Database connection errors:**

- Verify DATABASE_URL
- Check security group rules
- Confirm database is running
- Test connection manually

See Also
========

- :doc:`../installation/index` - Development installation
- :doc:`../architecture/overview` - Understanding the architecture
- :doc:`/reference/settings-reference` - Settings documentation
- `Django Deployment Checklist <https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/>`_
