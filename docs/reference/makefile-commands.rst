================
Makefile Commands
================

Complete reference for development Makefile commands.

Overview
========

Construbot includes a Makefile with convenient development commands.

**Location:** ``/Makefile`` (project root)

Docker Commands
===============

Development
-----------

**make dev**

Start development environment

.. code-block:: bash

   make dev
   # Starts: redis, postgres, mailhog, django
   # Uses: local settings, DEBUG=True

**make buildev**

Build and start development environment

.. code-block:: bash

   make buildev
   # Builds images, starts services, runs migrations

**make buildprod**

Build production environment

.. code-block:: bash

   make buildprod
   # Uses: production settings, DEBUG=False

Container Management
--------------------

**make down**

Stop all containers

.. code-block:: bash

   make down

**make clean**

Remove all containers

.. code-block:: bash

   make clean

**make cleandb**

Remove database containers and volumes

.. code-block:: bash

   make cleandb
   # WARNING: Deletes all data!

**make cleanhard**

Remove everything (containers, volumes, images)

.. code-block:: bash

   make cleanhard
   # WARNING: Complete cleanup!

Database Commands
=================

**make migrations**

Create and apply migrations

.. code-block:: bash

   make migrations
   # Runs: makemigrations && migrate

**make superuser**

Create Django superuser

.. code-block:: bash

   make superuser
   # Prompts for email and password

**make poblar**

Populate database with test data

.. code-block:: bash

   make poblar
   # Runs: python manage.py poblar

Development Tools
=================

**make shell**

Open Django shell

.. code-block:: bash

   make shell
   # Runs: python manage.py shell

**make runserver**

Run server without Docker

.. code-block:: bash

   make runserver
   # Sets USE_DOCKER=no
   # Runs: python manage.py runserver

Testing Commands
================

**make test**

Run full test suite with coverage

.. code-block:: bash

   make test
   # Runs: pytest with coverage report

**make localtest**

Run tests locally (no Docker)

.. code-block:: bash

   make localtest

**make warningtest**

Run tests with warnings enabled

.. code-block:: bash

   make warningtest

**make current**

Run tests tagged as 'current'

.. code-block:: bash

   make current
   # Runs: pytest -m current

Requirements Management
=======================

**make mkenv**

Sync local requirements

.. code-block:: bash

   make mkenv
   # Uses: pip-sync requirements/local.txt

**make pipcompile**

Compile requirements files

.. code-block:: bash

   make pipcompile
   # Compiles: base.in, local.in, test.in

Documentation Commands
======================

These commands are in ``docs/Makefile``:

**make html**

Build English documentation

.. code-block:: bash

   cd docs
   make html
   # Output: _build/html/

**make html-es**

Build Spanish documentation

.. code-block:: bash

   cd docs
   make html-es
   # Output: _build/html/es/

**make html-all**

Build both English and Spanish

.. code-block:: bash

   cd docs
   make html-all

**make update-translations**

Update translation files

.. code-block:: bash

   cd docs
   make update-translations
   # Extracts strings, updates .po files

**make livehtml**

Auto-rebuild documentation

.. code-block:: bash

   cd docs
   make livehtml
   # Starts server at http://127.0.0.1:8000

Common Workflows
================

Fresh Start
-----------

.. code-block:: bash

   make buildev
   make superuser
   make poblar

Daily Development
-----------------

.. code-block:: bash

   make dev         # Start environment
   make shell       # Django shell
   make test        # Run tests
   make down        # Stop when done

Reset Database
--------------

.. code-block:: bash

   make cleandb
   make buildev
   make superuser
   make poblar

Update Dependencies
-------------------

.. code-block:: bash

   # Edit requirements/*.in files
   make pipcompile
   make buildev  # Rebuild with new deps

Troubleshooting
===============

**Command not found:**

Ensure you're in project root directory.

**Permission denied:**

Run with sudo or fix Docker permissions:

.. code-block:: bash

   sudo usermod -aG docker $USER
   newgrp docker

**Port already in use:**

Stop conflicting services:

.. code-block:: bash

   lsof -ti:8000 | xargs kill -9

See Also
========

- :doc:`/developer/installation/docker-setup` - Docker setup guide
- :doc:`/developer/installation/local-setup` - Local setup guide
- :doc:`/contributor/testing/index` - Testing guide
