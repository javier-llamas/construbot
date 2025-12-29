============
Installation
============

This section covers how to install and set up Construbot for development. You can choose between Docker-based development (recommended) or local development.

Overview
========

Construbot supports two installation methods:

1. **Docker-based Development (Recommended)** - Containerized environment with all dependencies
2. **Local Development** - Traditional virtual environment setup

Both methods provide a complete development environment with:

- PostgreSQL database
- Redis for caching and Celery
- MailHog for email testing (Docker only)
- All Python dependencies

Prerequisites
=============

Docker Method
-------------

Required:

- Docker Desktop (includes Docker and Docker Compose)
- Git
- Make (usually pre-installed on macOS/Linux)

**Docker Desktop versions:**

- **macOS/Windows:** Download from https://www.docker.com/products/docker-desktop
- **Linux:** Install Docker Engine and Docker Compose separately

**Minimum requirements:**

- 4 GB RAM allocated to Docker
- 10 GB free disk space
- Docker Compose v2.0+

Local Method
------------

Required:

- Python 3.9.17 or higher
- PostgreSQL 12+
- Redis 6+
- Git
- pip and virtualenv

**Installation guides:**

- **macOS:** Use Homebrew: ``brew install python@3.9 postgresql redis``
- **Ubuntu/Debian:** ``sudo apt-get install python3.9 postgresql redis-server``
- **Windows:** Download installers from official websites

Quick Start
===========

Docker Method (5 minutes)
--------------------------

.. code-block:: bash

   # 1. Clone repository
   git clone https://github.com/javier-llamas/construbot.git
   cd construbot

   # 2. Build and start development environment
   make buildev

   # 3. Create superuser
   make superuser

   # 4. Access application
   open http://localhost:8000

**That's it!** The application is now running with:

- Django on http://localhost:8000
- MailHog on http://localhost:8025
- PostgreSQL on localhost:5432
- Redis on localhost:6379

Local Method (10 minutes)
--------------------------

.. code-block:: bash

   # 1. Clone repository
   git clone https://github.com/javier-llamas/construbot.git
   cd construbot

   # 2. Create virtual environment
   python3.9 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate

   # 3. Install dependencies
   pip install -r requirements/local.txt

   # 4. Set up environment variables
   cp .env.example .env
   # Edit .env with your database credentials

   # 5. Run migrations
   python manage.py migrate

   # 6. Create superuser
   python manage.py createsuperuser

   # 7. Run development server
   make runserver

   # 8. Access application
   open http://localhost:8000

Next Steps
==========

After installation:

1. **Populate test data:** Run ``make poblar`` to add sample data
2. **Explore the dashboard:** Log in with your superuser credentials
3. **Read the architecture docs:** :doc:`../architecture/overview`
4. **Check configuration options:** :doc:`configuration`

Detailed Guides
===============

.. toctree::
   :maxdepth: 2

   docker-setup
   local-setup
   requirements
   configuration

Troubleshooting
===============

Docker Issues
-------------

**"Port already in use" error:**

.. code-block:: bash

   # Find and stop conflicting services
   lsof -ti:8000 | xargs kill -9  # macOS/Linux
   # Or change ports in docker-compose.yml

**"No space left on device":**

.. code-block:: bash

   # Clean up Docker
   make cleanhard  # Warning: Removes all images and volumes
   docker system prune -a

**Containers won't start:**

.. code-block:: bash

   # Check logs
   docker-compose logs

   # Rebuild from scratch
   make clean
   make buildev

Local Installation Issues
--------------------------

**"pg_config executable not found":**

.. code-block:: bash

   # Install PostgreSQL development headers
   # macOS: brew install postgresql
   # Ubuntu: sudo apt-get install libpq-dev

**"Python.h: No such file":**

.. code-block:: bash

   # Install Python development headers
   # Ubuntu: sudo apt-get install python3.9-dev
   # macOS: Should be included with Python

**Database connection errors:**

Check your ``.env`` file:

.. code-block:: bash

   DATABASE_URL=postgresql://user:password@localhost:5432/construbot_dev

Make sure PostgreSQL is running:

.. code-block:: bash

   # macOS: brew services start postgresql
   # Ubuntu: sudo service postgresql start

Environment Variables
---------------------

**Missing .env file:**

Copy the example file:

.. code-block:: bash

   cp .env.example .env

**Required variables not set:**

Minimum required variables:

.. code-block:: bash

   DJANGO_SETTINGS_MODULE=construbot.config.settings.local
   DJANGO_DEBUG=True
   DATABASE_URL=postgresql://...
   DJANGO_SECRET_KEY=your-secret-key-here

See :doc:`configuration` for complete reference.

Common Questions
================

**Q: Which method should I use?**

A: Docker is recommended for most developers. It provides:

- Consistent environment across all platforms
- No need to install PostgreSQL/Redis locally
- Easy cleanup (``make clean``)
- Closer to production environment

Use local development if:

- You already have PostgreSQL/Redis installed
- You need to integrate with other local services
- You prefer traditional Python development

**Q: Can I switch between methods?**

A: Yes! The codebase is the same. Just change the ``USE_DOCKER`` environment variable.

**Q: How do I update my installation?**

A:

.. code-block:: bash

   git pull
   # Docker: make buildev
   # Local: pip install -r requirements/local.txt
   python manage.py migrate

**Q: Where is the database data stored?**

A:

- **Docker:** In a Docker volume named ``construbot_postgres_data``
- **Local:** In your PostgreSQL data directory (depends on installation)

To reset the database: ``make cleandb`` (Docker) or drop/recreate the database manually (local).

See Also
========

- :doc:`../architecture/settings-structure` - Understanding settings configuration
- :doc:`../deployment/index` - Production deployment guides
- :doc:`/contributor/development-setup` - Contributing to Construbot
- :doc:`/reference/makefile-commands` - Complete Makefile command reference
