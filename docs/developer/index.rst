=====================
Developer Documentation
=====================

Welcome to the Construbot Developer Documentation! This section provides technical information for developers who want to install, deploy, or extend Construbot.

.. note::
   **Looking for user documentation?** See the :doc:`/user-guide/index` instead.

Quick Links
===========

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 🚀 Installation
      :link: installation/index
      :link-type: doc

      Get Construbot running locally using Docker or virtual environment.

   .. grid-item-card:: 🌐 Deployment
      :link: deployment/index
      :link-type: doc

      Deploy to production on AWS EC2, Heroku, or your own infrastructure.

   .. grid-item-card:: 🏗️ Architecture
      :link: architecture/index
      :link-type: doc

      Understand the system architecture, settings, and design patterns.

   .. grid-item-card:: 📡 API Reference
      :link: api/index
      :link-type: doc

      REST API documentation with JWT authentication.

Technical Overview
==================

**Technology Stack:**

- **Framework:** Django 3.2.19
- **Language:** Python >=3.9.17
- **Database:** PostgreSQL
- **Cache/Queue:** Redis
- **Task Queue:** Celery 5.2.7
- **API:** Django REST Framework + SimpleJWT
- **Frontend:** Bootstrap 4 + jQuery

**Key Features:**

- Multi-tenant architecture (Customer → Company → User)
- Hierarchical data structures (django-treebeard)
- JWT-based API authentication
- Autocomplete widgets (django-autocomplete-light)
- PDF generation
- Excel import/export
- Celery task processing

Project Structure
=================

.. code-block:: text

   construbot/
   ├── construbot/
   │   ├── config/              # Django settings
   │   │   └── settings/
   │   │       ├── base.py
   │   │       ├── local.py
   │   │       ├── test.py
   │   │       └── production.py
   │   ├── users/               # Custom user model
   │   ├── proyectos/           # Core business logic
   │   ├── core/                # Shared utilities
   │   ├── api/                 # REST API
   │   ├── account_config/      # Account configuration
   │   ├── taskapp/             # Celery configuration
   │   ├── static/              # Static files
   │   ├── media/               # User uploads
   │   └── templates/           # Django templates
   ├── requirements/            # Dependencies
   ├── tests/                   # Test suite
   ├── docs/                    # Documentation
   ├── manage.py
   ├── setup.py
   └── Makefile                 # Development commands

Quick Start
===========

**For Docker:**

.. code-block:: bash

   # Clone repository
   git clone https://github.com/javier-llamas/construbot.git
   cd construbot

   # Build and start
   make buildev

   # Create superuser
   make superuser

   # Access at http://localhost:8000

**For Local Development:**

.. code-block:: bash

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate

   # Install dependencies
   pip install -r requirements/local.txt

   # Run migrations
   python manage.py migrate

   # Run server
   make runserver

**See:** :doc:`installation/index` for detailed instructions.

Development Workflow
====================

1. **Setup**: Install using Docker or local environment
2. **Configure**: Set environment variables in ``.env``
3. **Migrate**: Run database migrations
4. **Populate**: Use ``make poblar`` for test data
5. **Develop**: Make changes, run tests
6. **Test**: Run ``make test`` before committing
7. **Deploy**: Follow deployment guides

Documentation Sections
======================

.. toctree::
   :maxdepth: 2

   installation/index
   deployment/index
   architecture/index
   api/index
   models/index
   views/index
   forms/index
   management-commands/index
   utilities/index
   library-mode

Key Concepts for Developers
============================

Multi-Tenancy
-------------

Construbot uses a three-level hierarchy:

- **Customer** (users.models.Customer) - Top-level account
- **Company** (users.models.Company) - Business entity
- **User** (users.models.User) - Individual with permissions

All data models are scoped to a Company for isolation.

**Learn more:** :doc:`architecture/multi-tenancy`

Custom User Model
-----------------

``AUTH_USER_MODEL = 'users.User'``

- Email-based authentication (not username)
- Company relationships (ManyToMany)
- Permission levels (1-6)
- Currently active company tracking

**Learn more:** :doc:`models/users`

Settings Structure
------------------

Environment-based settings in ``construbot/config/settings/``:

- ``base.py`` - Shared configuration
- ``local.py`` - Development settings
- ``test.py`` - Testing configuration
- ``production.py`` - Production settings

Controlled via ``DJANGO_SETTINGS_MODULE`` environment variable.

**Learn more:** :doc:`architecture/settings-structure`

Hierarchical Models
-------------------

The Contrato (Contract) model uses django-treebeard's Materialized Path for hierarchical relationships:

- Parent contracts with sub-contracts
- Tree queries for financial aggregation
- Move operations for reorganization

**Learn more:** :doc:`models/proyectos`

API Authentication
------------------

REST API uses JWT tokens:

.. code-block:: bash

   # Obtain token
   curl -X POST /api/v1/api-token-auth/ \\
     -d "email=user@example.com&password=secret"

   # Use token
   curl -H "Authorization: Bearer <token>" \\
     /api/v1/...

**Learn more:** :doc:`api/authentication`

Library Mode
------------

Set ``CONSTRUBOT_AS_LIBRARY=True`` to:

- Disable standalone features (admin, accounts)
- Use Construbot as a Django app in your project
- Integrate with existing authentication

**Learn more:** :doc:`library-mode`

Development Tools
=================

Makefile Commands
-----------------

The project includes a comprehensive Makefile:

.. code-block:: bash

   make dev            # Start development environment
   make buildev        # Build and start with local settings
   make test           # Run full test suite with coverage
   make migrations     # Create and apply migrations
   make superuser      # Create Django superuser
   make poblar         # Populate database with test data
   make shell          # Run Django shell
   make clean          # Remove containers
   make cleandb        # Remove database
   make runserver      # Run without Docker

**Full reference:** :doc:`/reference/makefile-commands`

Testing
-------

.. code-block:: bash

   # Run all tests with coverage
   make test

   # Run with warnings
   make warningtest

   # Run specific tag
   make current  # Runs tests tagged with @tag('current')

   # Local testing (no Docker)
   make localtest

**Learn more:** :doc:`/contributor/testing/index`

Code Quality
------------

- **Style**: Follow PEP 8
- **Docstrings**: Google/NumPy style
- **Type Hints**: Encouraged but not required
- **Testing**: Aim for >80% coverage

**Learn more:** :doc:`/contributor/code-style`

Contributing
============

Want to contribute to Construbot?

1. **Fork** the repository
2. **Clone** your fork
3. **Create** a feature branch
4. **Make** your changes
5. **Test** thoroughly
6. **Submit** a pull request

**See:** :doc:`/contributor/index` for detailed guidelines.

Support & Resources
===================

- **GitHub Repository**: https://github.com/javier-llamas/construbot
- **Issue Tracker**: https://github.com/javier-llamas/construbot/issues
- **License**: GNU Affero General Public License v3 (AGPLv3)
- **Documentation**: https://construbot.readthedocs.io

Need Help?
==========

- **Installation Issues**: See :doc:`installation/index`
- **Deployment Problems**: Check :doc:`deployment/index`
- **API Questions**: Review :doc:`api/index`
- **Bug Reports**: :doc:`/contributor/issue-reporting`
