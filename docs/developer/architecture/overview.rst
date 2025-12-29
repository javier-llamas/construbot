========
Overview
========

High-level system architecture of Construbot.

.. note::
   **This page provides a quick overview.** For comprehensive architecture documentation with diagrams and code examples, see the :doc:`index`.

System Architecture
===================

Construbot follows a standard Django MTV (Model-Template-View) architecture with additional layers for API, background tasks, and caching.

Core Components
---------------

**Web Layer:**

- Nginx: Reverse proxy, SSL termination, static file serving
- Gunicorn: WSGI server running Django

**Application Layer:**

- Django 3.2.19: Web framework
- Django REST Framework: API layer
- Custom business logic in apps

**Data Layer:**

- PostgreSQL: Primary database
- Redis: Caching and message broker
- S3: Media file storage (production)

**Background Processing:**

- Celery: Asynchronous task queue
- Redis: Message broker

Key Design Patterns
===================

**Multi-Tenancy:**

Three-level hierarchy (Customer → Company → User) with company-scoped data isolation.

**Hierarchical Data:**

Tree structures using django-treebeard for contracts with parent/child relationships.

**Email Authentication:**

Custom auth backend using email instead of username.

**Permission Levels:**

Six-tier permission system (Auxiliar to Superusuario) for fine-grained access control.

Technology Stack
================

**Backend:**

.. code-block:: text

   Django 3.2.19 (Python 3.9.17+)
   ├── PostgreSQL 12+ (Database)
   ├── Redis 6+ (Cache/Queue)
   ├── Celery 5.2.7 (Tasks)
   └── DRF 3.13.1 (API)

**Key Libraries:**

- django-treebeard: Hierarchical models
- django-allauth: Authentication
- reportlab: PDF generation
- openpyxl: Excel import/export
- SimpleJWT: API authentication

Application Structure
=====================

**Main Apps:**

- ``users``: User management, companies, authentication
- ``proyectos``: Core business logic (contracts, estimates, counterparties)
- ``api``: REST API endpoints
- ``core``: Shared utilities
- ``account_config``: Company configuration

**Configuration:**

Settings split by environment (base, local, test, production) in ``construbot/config/settings/``.

See :doc:`settings-structure` for details.

Data Flow
=========

**Web Request:**

.. code-block:: text

   User → Nginx → Gunicorn → Django → PostgreSQL
                                   ↓
                                 Redis (Cache)

**API Request:**

.. code-block:: text

   Client → Nginx → Gunicorn → DRF (JWT Auth) → PostgreSQL

**Background Task:**

.. code-block:: text

   Django → Celery (via Redis) → Worker → Execute Task

Multi-Tenancy Model
===================

**Hierarchy:**

.. code-block:: python

   class Customer(models.Model):
       # Top-level account
       nombre = models.CharField(max_length=200)

   class Company(models.Model):
       # Business entity under customer
       customer = models.ForeignKey(Customer)
       nombre = models.CharField(max_length=200)

   class User(AbstractUser):
       # Individual user
       companies = models.ManyToManyField(Company)
       active_company = models.ForeignKey(Company)

**All business data** (contracts, estimates, etc.) is scoped to Company:

.. code-block:: python

   class Contrato(models.Model):
       company = models.ForeignKey(Company)  # Required
       # ... other fields

See :doc:`multi-tenancy` for complete details.

Security Architecture
=====================

**Authentication:**

- Email-based login (no usernames)
- Session-based for web
- JWT tokens for API

**Authorization:**

- Login required for all views
- Permission level checks
- Company-scoped data access

**Data Protection:**

- HTTPS/SSL in production
- CSRF protection
- Secure cookies (HttpOnly, Secure flags)
- Input validation and sanitization

See :doc:`authentication` for details.

Performance Strategy
====================

**Database:**

- Connection pooling
- Query optimization (select_related, prefetch_related)
- Atomic transactions

**Caching:**

- Redis cache backend
- Per-view caching
- Template fragment caching
- Query result caching

**Static Files:**

- WhiteNoise for serving
- Gzip/Brotli compression
- CDN for high traffic

**Background Tasks:**

- Celery for async operations
- Email sending
- PDF generation
- Scheduled tasks

Scalability
===========

**Vertical Scaling:**

Increase server resources (CPU, RAM, storage).

**Horizontal Scaling:**

- Load balancer (ALB/Nginx)
- Multiple application servers
- Managed database with read replicas (RDS)
- External cache (ElastiCache)
- S3 for media files

**Stateless design** enables easy horizontal scaling.

Development vs Production
=========================

**Development:**

- SQLite or local PostgreSQL
- Local Redis
- DEBUG=True
- Django serves static files
- Console email backend

**Production:**

- PostgreSQL (RDS recommended)
- Redis (ElastiCache recommended)
- DEBUG=False
- WhiteNoise/CDN for static files
- Production email service (Mailgun/SES)
- Sentry for error tracking

See :doc:`../installation/index` and :doc:`../deployment/index`.

Further Reading
===============

**Architecture Details:**

- :doc:`settings-structure` - Settings organization
- :doc:`multi-tenancy` - Multi-tenant design
- :doc:`authentication` - Auth system
- :doc:`permission-levels` - Permission system
- :doc:`database-schema` - Database design
- :doc:`url-structure` - URL routing

**Related Documentation:**

- :doc:`../installation/index` - Development setup
- :doc:`../deployment/index` - Production deployment
- :doc:`../api/index` - API documentation
- :doc:`../models/index` - Data models

**Comprehensive Overview:**

For detailed architecture information with code examples and diagrams, see :doc:`index`.
