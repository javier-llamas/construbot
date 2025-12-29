============
Architecture
============

Technical architecture and design patterns used in Construbot.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

Construbot is a Django-based construction management system built with modern patterns and best practices. This section explains the architectural decisions, data models, and system design.

.. toctree::
   :maxdepth: 2

   overview
   settings-structure
   multi-tenancy
   authentication
   permission-levels
   database-schema
   url-structure

Quick Reference
===============

Technology Stack
----------------

**Backend:**

- Django 3.2.19 (LTS)
- Python 3.9.17+
- PostgreSQL 12+
- Redis 6+

**Task Queue:**

- Celery 5.2.7
- Redis broker

**API:**

- Django REST Framework 3.13.1
- SimpleJWT 5.2.0

**Key Libraries:**

- django-treebeard 4.5.1 (hierarchical models)
- django-allauth 0.51.0 (authentication)
- django-autocomplete-light 3.9.4 (autocomplete widgets)
- reportlab 3.6.12 (PDF generation)
- openpyxl 3.0.10 (Excel import/export)

System Components
=================

Application Layer
-----------------

.. code-block:: text

   ┌──────────────────────────────────────────┐
   │         Web Clients / API Clients        │
   └────────────────┬─────────────────────────┘
                    │
                    ▼
   ┌──────────────────────────────────────────┐
   │      Nginx (Reverse Proxy / SSL)         │
   └────────────────┬─────────────────────────┘
                    │
                    ▼
   ┌──────────────────────────────────────────┐
   │    Gunicorn (WSGI Server)                │
   │    ┌──────────────────────────────┐      │
   │    │  Django Application          │      │
   │    │  ├─ proyectos (core logic)   │      │
   │    │  ├─ users (auth & accounts)  │      │
   │    │  ├─ api (REST endpoints)     │      │
   │    │  └─ core (utilities)         │      │
   │    └──────────────────────────────┘      │
   └────────────────┬─────────────────────────┘
                    │
          ┌─────────┴──────────┐
          ▼                    ▼
   ┌──────────────┐    ┌──────────────┐
   │  PostgreSQL  │    │    Redis     │
   │  (Database)  │    │(Cache/Queue) │
   └──────────────┘    └──────┬───────┘
                              │
                              ▼
                       ┌──────────────┐
                       │Celery Workers│
                       │(Background)  │
                       └──────────────┘

Data Flow
---------

**User Request:**

1. User accesses application → Nginx
2. Nginx proxies to Gunicorn
3. Gunicorn runs Django request/response cycle
4. Django queries PostgreSQL for data
5. Django uses Redis for caching
6. Response rendered and returned

**Background Task:**

1. User action triggers task → Celery delay()
2. Task queued in Redis
3. Celery worker picks up task
4. Worker executes task (e.g., send email, generate PDF)
5. Result stored in Redis (optional)

Application Structure
=====================

Django Apps
-----------

**construbot.users** - User management

- Custom User model (email-based auth)
- Company and Customer models
- Permission levels (NivelAcceso)
- Authentication backends

**construbot.proyectos** - Core business logic

- Contract management (Contrato)
- Counterparty management (Contraparte)
- Estimate tracking (Estimate)
- Hierarchical data structures
- Financial calculations

**construbot.api** - REST API

- JWT authentication
- API endpoints for mobile/external access
- Serializers and viewsets
- Data migration endpoints

**construbot.core** - Shared utilities

- Base models and mixins
- Custom authentication backend
- Utility functions
- Shared templates

**construbot.account_config** - Account configuration

- Company-specific settings
- Custom login forms
- Account preferences

**construbot.taskapp** - Celery configuration

- Celery app initialization
- Task definitions
- Periodic task setup

Directory Structure
-------------------

.. code-block:: text

   construbot/
   ├── construbot/                   # Main Django project
   │   ├── config/                   # Project configuration
   │   │   ├── settings/             # Environment-specific settings
   │   │   │   ├── base.py           # Shared settings
   │   │   │   ├── local.py          # Development
   │   │   │   ├── test.py           # Testing
   │   │   │   └── production.py     # Production
   │   │   ├── urls.py               # Root URL configuration
   │   │   └── wsgi.py               # WSGI application
   │   │
   │   ├── users/                    # User management app
   │   │   ├── models.py             # User, Company, Customer
   │   │   ├── views.py              # User views
   │   │   ├── forms.py              # User forms
   │   │   └── admin.py              # Admin interface
   │   │
   │   ├── proyectos/                # Core business app
   │   │   ├── models.py             # Business models
   │   │   ├── views.py              # Business views
   │   │   ├── forms.py              # Business forms
   │   │   └── migrations/           # Database migrations
   │   │
   │   ├── api/                      # REST API app
   │   │   ├── views.py              # API viewsets
   │   │   ├── serializers.py        # Data serializers
   │   │   └── urls.py               # API routes
   │   │
   │   ├── core/                     # Shared utilities
   │   │   ├── models.py             # Base models
   │   │   ├── backends.py           # Auth backend
   │   │   └── utils.py              # Utility functions
   │   │
   │   ├── static/                   # Static files
   │   │   ├── css/                  # Stylesheets
   │   │   ├── js/                   # JavaScript
   │   │   └── images/               # Images
   │   │
   │   ├── templates/                # Django templates
   │   │   ├── base.html             # Base template
   │   │   └── ...                   # App templates
   │   │
   │   └── media/                    # User uploads
   │
   ├── requirements/                 # Dependencies
   │   ├── base.txt                  # Core dependencies
   │   ├── local.txt                 # Development
   │   ├── test.txt                  # Testing
   │   └── production.txt            # Production
   │
   ├── tests/                        # Test suite
   │   └── ...                       # Test files
   │
   ├── docs/                         # Documentation
   │   └── ...                       # Documentation files
   │
   ├── compose/                      # Docker configuration
   │   ├── local/                    # Local development
   │   └── production/               # Production
   │
   ├── manage.py                     # Django management script
   ├── setup.py                      # Package setup
   ├── docker-compose.yml            # Docker Compose config
   └── Makefile                      # Development commands

Design Patterns
===============

Multi-Tenancy
-------------

**Three-level hierarchy:**

.. code-block:: text

   Customer (Top-level account)
   └── Company (Business entity)
       └── User (Individual with permissions)

**Data isolation:**

- All business data scoped to Company
- Users can belong to multiple Companies
- Active company tracked in session

See :doc:`multi-tenancy` for details.

Hierarchical Models
-------------------

**django-treebeard Materialized Path:**

Contracts (Contrato) form tree structures:

.. code-block:: text

   Main Contract
   ├── Subcontract 1
   │   ├── Sub-subcontract 1.1
   │   └── Sub-subcontract 1.2
   └── Subcontract 2

**Benefits:**

- Efficient parent/child queries
- Tree aggregations (sum amounts)
- Move operations
- Path-based queries

**Implementation:**

.. code-block:: python

   from treebeard.mp_tree import MP_Node

   class Contrato(MP_Node):
       # Inherits: path, depth, numchild
       # Methods: get_children(), get_ancestors(), etc.

Custom Authentication
---------------------

**Email-based authentication:**

- No username field
- Email as unique identifier
- Custom authentication backend

**Multi-company support:**

- User can access multiple companies
- Company switch without re-login
- Per-company permissions

See :doc:`authentication` for details.

Permission System
-----------------

**Six permission levels (NIVELES_ACCESO):**

1. Auxiliar (1) - View only
2. Coordinador (2) - Create/edit
3. Director (3) - Full CRUD
4. Corporativo (4) - Cross-company
5. Soporte (5) - Support access
6. Superusuario (6) - Full system access

See :doc:`permission-levels` for details.

Data Access Patterns
====================

Query Optimization
------------------

**Select Related (foreign keys):**

.. code-block:: python

   # Avoid N+1 queries
   contratos = Contrato.objects.select_related('contraparte', 'company')

**Prefetch Related (many-to-many):**

.. code-block:: python

   # Optimize related objects
   users = User.objects.prefetch_related('companies', 'user_companies')

**Database indexes:**

.. code-block:: python

   class Contrato(models.Model):
       folio = models.CharField(max_length=100, db_index=True)

       class Meta:
           indexes = [
               models.Index(fields=['company', 'fecha_inicio']),
           ]

Caching Strategy
----------------

**Per-view caching:**

.. code-block:: python

   from django.views.decorators.cache import cache_page

   @cache_page(60 * 15)  # 15 minutes
   def dashboard_view(request):
       ...

**Template fragment caching:**

.. code-block:: django

   {% load cache %}
   {% cache 600 sidebar request.user.id %}
       ... expensive template code ...
   {% endcache %}

**Query result caching:**

.. code-block:: python

   from django.core.cache import cache

   def get_company_stats(company_id):
       key = f'company_stats_{company_id}'
       stats = cache.get(key)
       if stats is None:
           stats = calculate_stats(company_id)
           cache.set(key, stats, 3600)  # 1 hour
       return stats

Atomic Transactions
-------------------

**Enabled by default:**

.. code-block:: python

   # In settings/base.py
   DATABASES = {
       'default': {
           ...
           'ATOMIC_REQUESTS': True,
       }
   }

**Manual transaction control:**

.. code-block:: python

   from django.db import transaction

   @transaction.atomic
   def create_contract_with_concepts(contract_data, concepts_data):
       contract = Contrato.objects.create(**contract_data)
       for concept_data in concepts_data:
           Concept.objects.create(contract=contract, **concept_data)
       return contract

API Design
==========

REST API Structure
------------------

**Base URL:** ``/api/v1/``

**Authentication:** JWT tokens

**Endpoints:**

.. code-block:: text

   POST   /api/v1/api-token-auth/        # Obtain token
   POST   /api/v1/api-token-refresh/     # Refresh token
   GET    /api/v1/contracts/             # List contracts
   POST   /api/v1/contracts/             # Create contract
   GET    /api/v1/contracts/:id/         # Retrieve contract
   PUT    /api/v1/contracts/:id/         # Update contract
   DELETE /api/v1/contracts/:id/         # Delete contract

**Response format:**

.. code-block:: json

   {
     "count": 100,
     "next": "http://api.example.com/api/v1/contracts/?page=2",
     "previous": null,
     "results": [...]
   }

See :doc:`../api/index` for complete API documentation.

Security Architecture
=====================

Authentication Flow
-------------------

**Web application:**

1. User submits email/password
2. Backend authenticates against User model
3. Session created with company context
4. User redirected to dashboard

**API:**

1. Client posts credentials to ``/api-token-auth/``
2. Server validates and returns JWT token
3. Client includes token in ``Authorization: Bearer <token>`` header
4. Server validates token on each request

Authorization Layers
--------------------

**1. Authentication required:**

.. code-block:: python

   from django.contrib.auth.decorators import login_required

   @login_required
   def view(request):
       ...

**2. Permission level check:**

.. code-block:: python

   def director_required(view_func):
       def wrapper(request, *args, **kwargs):
           if request.user.nivel_acceso.nivel < 3:
               return HttpResponseForbidden()
           return view_func(request, *args, **kwargs)
       return wrapper

**3. Company-scoped data:**

.. code-block:: python

   # Always filter by active company
   contratos = Contrato.objects.filter(company=request.user.active_company)

See :doc:`authentication` and :doc:`permission-levels` for details.

Performance Considerations
==========================

Database
--------

- Connection pooling (``CONN_MAX_AGE``)
- Query optimization (select_related/prefetch_related)
- Database indexes on frequently queried fields
- Atomic requests for data integrity

Caching
-------

- Redis for cache backend
- Session storage in cache
- Query result caching
- Template fragment caching

Static Files
------------

- WhiteNoise for efficient serving
- Gzip/Brotli compression
- Far-future cache headers
- CDN for high-traffic deployments

Background Tasks
----------------

- Celery for asynchronous operations
- Email sending in background
- PDF generation in background
- Scheduled tasks with Celery Beat

Scalability
===========

Vertical Scaling
----------------

- Increase server CPU/RAM
- Upgrade database instance
- Add Redis memory

Horizontal Scaling
------------------

- Multiple Django application servers
- Load balancer (ALB/Nginx)
- Managed database (RDS with read replicas)
- External cache (ElastiCache)
- S3 for media files

**Stateless application servers** enable easy horizontal scaling.

Monitoring Points
=================

Application Metrics
-------------------

- Request/response times
- Error rates (4xx, 5xx)
- Database query performance
- Cache hit/miss ratio
- Celery task queue length

Infrastructure Metrics
----------------------

- CPU usage
- Memory usage
- Disk I/O
- Network traffic
- Database connections

Business Metrics
----------------

- Active users
- Contracts created
- Estimates generated
- PDF downloads
- API usage

See :doc:`../deployment/index` for monitoring setup.

Development Workflow
====================

Local Development
-----------------

1. Use Docker Compose for consistent environment
2. Run ``make dev`` to start services
3. Code changes auto-reload (Django development server)
4. Use ``make shell`` for Django shell
5. Run ``make test`` before committing

See :doc:`../installation/index` for setup.

Testing Strategy
----------------

- Unit tests for models and utilities
- Integration tests for views
- API tests for REST endpoints
- Coverage target: >80%

See :doc:`/contributor/testing/index` for testing guide.

Deployment Process
------------------

1. Run tests (``make test``)
2. Build Docker images
3. Run database migrations
4. Collect static files
5. Restart application servers
6. Verify deployment

See :doc:`../deployment/index` for deployment guide.

See Also
========

- :doc:`settings-structure` - Settings organization
- :doc:`multi-tenancy` - Multi-tenant architecture
- :doc:`database-schema` - Database design
- :doc:`url-structure` - URL routing
- :doc:`../api/index` - API documentation
