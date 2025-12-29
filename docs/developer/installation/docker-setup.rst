============
Docker Setup
============

Complete guide to setting up Construbot with Docker for local development.

.. note::
   **Recommended Method:** Docker provides the easiest and most consistent development environment across all platforms.

Overview
========

The Docker development environment includes:

- **Django:** Web application (port 8000)
- **PostgreSQL:** Database (port 5432)
- **Redis:** Cache and Celery broker (port 6379)
- **MailHog:** Email testing interface (port 8025)
- **Celery Worker:** Background task processing

All services are orchestrated using Docker Compose with automatic dependency management.

Installation
============

Step 1: Install Docker Desktop
-------------------------------

**macOS:**

.. code-block:: bash

   # Using Homebrew
   brew install --cask docker

   # Or download from: https://www.docker.com/products/docker-desktop

**Windows:**

Download Docker Desktop from https://www.docker.com/products/docker-desktop

**Linux (Ubuntu/Debian):**

.. code-block:: bash

   # Install Docker Engine
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh

   # Install Docker Compose
   sudo apt-get install docker-compose-plugin

   # Add your user to docker group
   sudo usermod -aG docker $USER
   newgrp docker

**Verify installation:**

.. code-block:: bash

   docker --version
   # Should show: Docker version 20.10+ or higher

   docker-compose --version
   # Should show: Docker Compose version 2.0+ or higher

Step 2: Clone Repository
-------------------------

.. code-block:: bash

   git clone https://github.com/javier-llamas/construbot.git
   cd construbot

Step 3: Build and Start
------------------------

The project includes a Makefile with convenient commands:

.. code-block:: bash

   # Build images and start with development settings
   make buildev

This command:

1. Modifies ``.env`` to set ``DJANGO_SETTINGS_MODULE=construbot.config.settings.local``
2. Sets ``DJANGO_DEBUG=True``
3. Builds Docker images
4. Starts all services (postgres, redis, mailhog, django)
5. Runs database migrations
6. Collects static files

**Expected output:**

.. code-block:: text

   Creating network "construbot_default" with the default driver
   Creating volume "construbot_postgres_data" with default driver
   Creating construbot_postgres_1 ... done
   Creating construbot_redis_1    ... done
   Creating construbot_mailhog_1  ... done
   Creating construbot_django_1   ... done
   Running migrations...
   Operations to perform:
     Apply all migrations: ...
   Applying ...
   Collecting static files...

Step 4: Create Superuser
-------------------------

.. code-block:: bash

   make superuser

You'll be prompted for:

- **Email:** Your admin email (used for login)
- **Password:** Secure password
- **Password (again):** Confirmation

.. code-block:: text

   Email: admin@example.com
   Password:
   Password (again):
   Superuser created successfully.

Step 5: Access Application
---------------------------

Open your browser to:

- **Django Application:** http://localhost:8000
- **MailHog Interface:** http://localhost:8025 (email testing)

Login with the superuser credentials you just created.

Docker Compose Configuration
=============================

The project uses ``docker-compose.yml`` for service orchestration.

Services Overview
-----------------

**django:**

.. code-block:: yaml

   django:
     build:
       context: .
       dockerfile: ./compose/local/django/Dockerfile
     image: construbot_local_django
     container_name: construbot_django
     depends_on:
       - postgres
       - redis
       - mailhog
     volumes:
       - .:/app:z
     env_file:
       - ./.env
     ports:
       - "8000:8000"
     command: /start

- Runs Django development server with auto-reload
- Mounts current directory for live code changes
- Exposes port 8000

**postgres:**

.. code-block:: yaml

   postgres:
     image: postgres:12-alpine
     container_name: construbot_postgres
     volumes:
       - postgres_data:/var/lib/postgresql/data
     environment:
       - POSTGRES_HOST=postgres
       - POSTGRES_PORT=5432
       - POSTGRES_DB=construbot
       - POSTGRES_USER=debug
       - POSTGRES_PASSWORD=debug

- Uses PostgreSQL 12 with Alpine Linux
- Persistent data in named volume
- Default development credentials

**redis:**

.. code-block:: yaml

   redis:
     image: redis:6-alpine
     container_name: construbot_redis

- Redis 6 for caching and Celery broker
- No persistence configured (development only)

**mailhog:**

.. code-block:: yaml

   mailhog:
     image: mailhog/mailhog:v1.0.0
     container_name: construbot_mailhog
     ports:
       - "8025:8025"

- Catches all outgoing emails
- Web UI at http://localhost:8025

Environment Configuration
=========================

The ``.env`` file controls environment-specific settings.

Development Environment Variables
----------------------------------

When you run ``make buildev``, these are set automatically:

.. code-block:: bash

   # Django Settings
   DJANGO_SETTINGS_MODULE=construbot.config.settings.local
   DJANGO_DEBUG=True
   DJANGO_READ_DOT_ENV_FILE=True

   # Docker
   USE_DOCKER=yes

   # Database
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   POSTGRES_DB=construbot
   POSTGRES_USER=debug
   POSTGRES_PASSWORD=debug

   # Redis
   REDIS_URL=redis://redis:6379/0

   # Email (MailHog)
   DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=mailhog
   EMAIL_PORT=1025

Manual Configuration
--------------------

To customize settings, edit ``.env``:

.. code-block:: bash

   # Copy example file if needed
   cp .env.example .env

   # Edit with your preferred editor
   nano .env

See :doc:`configuration` for complete variable reference.

Development Workflow
====================

Starting the Environment
------------------------

.. code-block:: bash

   # Start all services
   make dev

   # Or use docker-compose directly
   docker-compose up

**This starts services without rebuilding.** Use when:

- You've already run ``make buildev``
- No dependencies have changed
- You just want to start the containers

Stopping the Environment
-------------------------

.. code-block:: bash

   # Stop all containers
   make down

   # Or: Ctrl+C in the terminal running docker-compose up

Database Migrations
-------------------

.. code-block:: bash

   # Create and apply migrations
   make migrations

   # Or run manually:
   docker-compose run --rm django python manage.py makemigrations
   docker-compose run --rm django python manage.py migrate

Accessing Django Shell
-----------------------

.. code-block:: bash

   # Django shell
   make shell

   # Or:
   docker-compose run --rm django python manage.py shell

.. code-block:: python

   >>> from construbot.users.models import User
   >>> User.objects.count()
   1

Running Management Commands
----------------------------

.. code-block:: bash

   # Populate test data
   make poblar

   # Or run any Django command:
   docker-compose run --rm django python manage.py <command>

Viewing Logs
------------

.. code-block:: bash

   # All services
   docker-compose logs

   # Specific service
   docker-compose logs django

   # Follow logs (tail -f)
   docker-compose logs -f django

Rebuilding Images
-----------------

.. code-block:: bash

   # Rebuild all images
   make buildev

   # Force rebuild without cache
   docker-compose build --no-cache

**When to rebuild:**

- After changing ``requirements/*.txt``
- After modifying Dockerfiles
- After pulling updates from git with dependency changes

Testing in Docker
=================

Running Tests
-------------

.. code-block:: bash

   # Full test suite with coverage
   make test

   # Tests with warnings
   make warningtest

   # Specific test tag
   make current  # Runs tests tagged with @tag('current')

Test Configuration
------------------

Tests use ``construbot.config.settings.test`` which:

- Uses an in-memory SQLite database (faster)
- Disables migrations for speed
- Configures test-specific settings

See :doc:`/contributor/testing/running-tests` for more details.

Cleanup and Reset
=================

Remove Containers
-----------------

.. code-block:: bash

   # Stop and remove containers
   make clean

   # Or:
   docker-compose down

**This preserves:**

- Database data (in volume)
- Built images

Reset Database
--------------

.. code-block:: bash

   # Remove database volume
   make cleandb

   # Then rebuild:
   make buildev
   make superuser

**Warning:** This deletes all data!

Complete Cleanup
----------------

.. code-block:: bash

   # Remove EVERYTHING (containers, volumes, images)
   make cleanhard

**Warning:** This removes:

- All containers
- All volumes (database data)
- All built images
- You'll need to run ``make buildev`` to start fresh

Troubleshooting
===============

Port Conflicts
--------------

**Error:** "Port 8000 is already allocated"

**Solution 1:** Stop conflicting service

.. code-block:: bash

   # macOS/Linux
   lsof -ti:8000 | xargs kill -9

   # Or find process ID
   lsof -i:8000

**Solution 2:** Change port in ``docker-compose.yml``

.. code-block:: yaml

   django:
     ports:
       - "8001:8000"  # Changed from 8000:8000

Then access at http://localhost:8001

Container Won't Start
---------------------

**Check logs:**

.. code-block:: bash

   docker-compose logs django

**Common issues:**

1. **Database not ready:** Wait a few seconds, Django will retry
2. **Migration errors:** Run ``make migrations``
3. **Missing dependencies:** Run ``make buildev`` to rebuild

Volume Permission Issues
-------------------------

**Error:** "Permission denied" when accessing files

**Solution (Linux):**

.. code-block:: bash

   # Fix file ownership
   sudo chown -R $USER:$USER .

   # Or run Docker as root (not recommended)

Database Connection Errors
---------------------------

**Error:** "could not connect to server"

**Check postgres is running:**

.. code-block:: bash

   docker-compose ps postgres

**Restart postgres:**

.. code-block:: bash

   docker-compose restart postgres

**Check DATABASE_URL in .env:**

.. code-block:: bash

   # Should be:
   DATABASE_URL=postgresql://debug:debug@postgres:5432/construbot

Out of Disk Space
-----------------

**Error:** "No space left on device"

**Clean up Docker:**

.. code-block:: bash

   # Remove unused images and containers
   docker system prune -a

   # Check Docker disk usage
   docker system df

   # If needed, increase Docker Desktop disk allocation
   # Docker Desktop → Preferences → Resources → Disk image size

Advanced Topics
===============

Custom Docker Compose Override
-------------------------------

Create ``docker-compose.override.yml`` for local customizations:

.. code-block:: yaml

   version: '3'

   services:
     django:
       ports:
         - "8001:8000"  # Custom port
       environment:
         - CUSTOM_VAR=value

This file is git-ignored and won't be committed.

Running Celery Worker
----------------------

The project includes Celery for background tasks. To run a worker:

.. code-block:: bash

   # In a separate terminal
   docker-compose run --rm django celery -A construbot.taskapp worker -l info

Or add to ``docker-compose.yml``:

.. code-block:: yaml

   celeryworker:
     <<: *django
     container_name: construbot_celeryworker
     depends_on:
       - redis
       - postgres
     ports: []
     command: /start-celeryworker

Debugging with pdb
------------------

To use Python's debugger:

.. code-block:: bash

   # Start in foreground with stdin attached
   docker-compose run --rm --service-ports django

Add breakpoint in code:

.. code-block:: python

   import pdb; pdb.set_trace()

When the breakpoint hits, you'll get an interactive debugger in your terminal.

IDE Integration
---------------

**PyCharm Professional:**

1. Configure Python Interpreter → Docker Compose
2. Set service: ``django``
3. PyCharm will automatically use the Docker environment

**VS Code:**

1. Install "Remote - Containers" extension
2. Create ``.devcontainer/devcontainer.json``
3. Reopen in container

**Vim/Neovim:**

Set up LSP to use Docker:

.. code-block:: bash

   # Run language server in container
   docker-compose exec django pylsp

Performance Optimization
========================

macOS File Sharing
------------------

Docker on macOS can be slow with large codebases. Optimize with:

.. code-block:: yaml

   django:
     volumes:
       - .:/app:cached  # Use cached consistency mode

**consistency modes:**

- ``cached`` - Host writes are delayed to container (faster reads)
- ``delegated`` - Container writes are delayed to host (faster writes)
- ``consistent`` - Synchronous (default, slowest)

Linux Performance
-----------------

Docker on Linux has native performance, no tuning needed.

Windows (WSL2)
--------------

Use WSL2 backend for best performance:

1. Docker Desktop → Settings → General → Use WSL2
2. Clone repo inside WSL2 filesystem (not /mnt/c/)

See Also
========

- :doc:`local-setup` - Local development without Docker
- :doc:`configuration` - Environment variable reference
- :doc:`../deployment/docker-compose` - Production Docker setup
- :doc:`/reference/makefile-commands` - Complete Makefile reference
