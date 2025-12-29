===========
Local Setup
===========

Guide for setting up Construbot in a local development environment without Docker.

.. note::
   **Consider Docker:** Docker setup is recommended for most developers. Use local setup if you prefer traditional Python development or need to integrate with other local services.

Overview
========

Local development requires installing and configuring:

1. Python 3.9.17+
2. PostgreSQL 12+
3. Redis 6+
4. Python dependencies

You'll create a virtual environment and run services directly on your machine.

Prerequisites
=============

System Requirements
-------------------

**Python 3.9.17 or higher:**

.. code-block:: bash

   # Check version
   python3 --version
   # Should show: Python 3.9.17 or higher

**Installation:**

.. code-block:: bash

   # macOS (using Homebrew)
   brew install python@3.9

   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3.9 python3.9-venv python3.9-dev

   # Windows
   # Download from: https://www.python.org/downloads/

**PostgreSQL 12+:**

.. code-block:: bash

   # Check if installed
   psql --version

**Installation:**

.. code-block:: bash

   # macOS
   brew install postgresql@12
   brew services start postgresql@12

   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib libpq-dev

   # Windows
   # Download from: https://www.postgresql.org/download/windows/

**Redis 6+:**

.. code-block:: bash

   # Check if installed
   redis-cli --version

**Installation:**

.. code-block:: bash

   # macOS
   brew install redis
   brew services start redis

   # Ubuntu/Debian
   sudo apt-get install redis-server
   sudo systemctl start redis

   # Windows
   # Use WSL or download from: https://github.com/microsoftarchive/redis/releases

Development Tools
-----------------

**Git:**

.. code-block:: bash

   git --version

**pip and virtualenv:**

.. code-block:: bash

   # Should be included with Python
   pip3 --version
   python3 -m venv --help

Installation Steps
==================

Step 1: Clone Repository
-------------------------

.. code-block:: bash

   git clone https://github.com/javier-llamas/construbot.git
   cd construbot

Step 2: Create Virtual Environment
-----------------------------------

.. code-block:: bash

   # Create virtual environment
   python3.9 -m venv venv

   # Activate virtual environment
   # macOS/Linux:
   source venv/bin/activate

   # Windows:
   venv\\Scripts\\activate

Your prompt should change to show ``(venv)``:

.. code-block:: bash

   (venv) user@computer:~/construbot$

.. note::
   **Remember to activate:** You must activate the virtual environment every time you work on the project. Add ``source venv/bin/activate`` to your shell profile for automatic activation.

Step 3: Install Python Dependencies
------------------------------------

.. code-block:: bash

   # Upgrade pip
   pip install --upgrade pip

   # Install local development dependencies
   pip install -r requirements/local.txt

This installs:

- Django 3.2.19 and all extensions
- Development tools (pytest, coverage, django-debug-toolbar)
- Database drivers (psycopg2)
- All project dependencies

**Expected output:**

.. code-block:: text

   Collecting django==3.2.19
   Collecting djangorestframework==3.13.1
   ...
   Successfully installed ...

**Verify installation:**

.. code-block:: bash

   python -c "import django; print(django.get_version())"
   # Should show: 3.2.19

Step 4: Configure Database
---------------------------

**Create PostgreSQL database:**

.. code-block:: bash

   # Connect to PostgreSQL as superuser
   # macOS/Linux:
   psql postgres

   # Ubuntu (if above doesn't work):
   sudo -u postgres psql

**In PostgreSQL console:**

.. code-block:: sql

   -- Create database
   CREATE DATABASE construbot_dev;

   -- Create user
   CREATE USER construbot_user WITH PASSWORD 'construbot_pass';

   -- Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE construbot_dev TO construbot_user;

   -- Exit
   \\q

**Verify connection:**

.. code-block:: bash

   psql -h localhost -U construbot_user -d construbot_dev
   # Enter password: construbot_pass

If successful, you'll see the PostgreSQL prompt. Type ``\\q`` to exit.

Step 5: Configure Environment Variables
----------------------------------------

**Create .env file:**

.. code-block:: bash

   # Copy example file
   cp .env.example .env

   # Edit with your preferred editor
   nano .env

**Required settings for local development:**

.. code-block:: bash

   # Django Settings
   DJANGO_SETTINGS_MODULE=construbot.config.settings.local
   DJANGO_DEBUG=True
   DJANGO_READ_DOT_ENV_FILE=True
   DJANGO_SECRET_KEY=your-secret-key-here-change-in-production

   # Docker (set to no for local development)
   USE_DOCKER=no

   # Database
   DATABASE_URL=postgresql://construbot_user:construbot_pass@localhost:5432/construbot_dev

   # Redis
   REDIS_URL=redis://localhost:6379/0

   # Email (console backend for development)
   DJANGO_EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

.. note::
   **Generate SECRET_KEY:** Use Django's secret key generator:

   .. code-block:: bash

      python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

**Alternative: Use environment exports (temporary):**

.. code-block:: bash

   export DJANGO_SETTINGS_MODULE=construbot.config.settings.local
   export DJANGO_DEBUG=True
   export DATABASE_URL=postgresql://construbot_user:construbot_pass@localhost:5432/construbot_dev

These are lost when you close the terminal.

Step 6: Run Database Migrations
--------------------------------

.. code-block:: bash

   python manage.py migrate

**Expected output:**

.. code-block:: text

   Operations to perform:
     Apply all migrations: account, account_config, admin, auth, contenttypes, ...
   Running migrations:
     Applying contenttypes.0001_initial... OK
     Applying auth.0001_initial... OK
     Applying users.0001_initial... OK
     ...

**Verify tables were created:**

.. code-block:: bash

   psql -h localhost -U construbot_user -d construbot_dev -c "\\dt"

You should see a list of Django tables.

Step 7: Create Superuser
-------------------------

.. code-block:: bash

   python manage.py createsuperuser

**Prompts:**

.. code-block:: text

   Email: admin@example.com
   Password:
   Password (again):
   Superuser created successfully.

.. note::
   **Email as username:** Construbot uses email for authentication, not traditional usernames.

Step 8: Collect Static Files
-----------------------------

.. code-block:: bash

   python manage.py collectstatic --no-input

This copies static files (CSS, JavaScript, images) to the ``staticfiles/`` directory.

Step 9: Run Development Server
-------------------------------

.. code-block:: bash

   # Using Makefile (recommended)
   make runserver

   # Or manually:
   python manage.py runserver

**Expected output:**

.. code-block:: text

   Watching for file changes with StatReloader
   Performing system checks...

   System check identified no issues (0 silenced).
   December 29, 2025 - 14:30:00
   Django version 3.2.19, using settings 'construbot.config.settings.local'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.

**Access the application:**

Open http://localhost:8000 in your browser and log in with your superuser credentials.

Development Workflow
====================

Daily Startup
-------------

.. code-block:: bash

   # 1. Navigate to project
   cd ~/construbot

   # 2. Activate virtual environment
   source venv/bin/activate

   # 3. Start Redis (if not running as service)
   redis-server &

   # 4. Start PostgreSQL (if not running as service)
   # macOS: brew services start postgresql
   # Linux: sudo systemctl start postgresql

   # 5. Run Django development server
   make runserver

Database Migrations
-------------------

**After modifying models:**

.. code-block:: bash

   # Create migration files
   python manage.py makemigrations

   # Apply migrations
   python manage.py migrate

**Check migration status:**

.. code-block:: bash

   python manage.py showmigrations

Django Shell
------------

.. code-block:: bash

   python manage.py shell

.. code-block:: python

   >>> from construbot.users.models import User
   >>> User.objects.all()
   <QuerySet [<User: admin@example.com>]>

Management Commands
-------------------

**Populate test data:**

.. code-block:: bash

   python manage.py poblar

**Create another superuser:**

.. code-block:: bash

   python manage.py createsuperuser

**Run custom commands:**

.. code-block:: bash

   python manage.py <command_name>

Static Files
------------

**During development:**

Django serves static files automatically with ``DEBUG=True``. No action needed.

**After adding/modifying static files:**

.. code-block:: bash

   python manage.py collectstatic

Testing
=======

Running Tests
-------------

.. code-block:: bash

   # Full test suite with coverage
   make localtest

   # Or manually:
   pytest

   # Run specific test file
   pytest tests/test_users.py

   # Run with coverage report
   pytest --cov=construbot --cov-report=html

**View coverage report:**

.. code-block:: bash

   open htmlcov/index.html

Test Configuration
------------------

Local tests use ``construbot.config.settings.test`` which:

- Uses in-memory SQLite database
- Disables migrations for speed
- Sets test-specific configurations

See :doc:`/contributor/testing/running-tests` for details.

Running Celery
==============

For background task processing:

**Start Celery worker:**

.. code-block:: bash

   # In a separate terminal
   celery -A construbot.taskapp worker -l info

**Monitor tasks:**

.. code-block:: bash

   # Celery flower (task monitoring web UI)
   pip install flower
   celery -A construbot.taskapp flower

Access Flower at http://localhost:5555

Database Management
===================

Backup Database
---------------

.. code-block:: bash

   # Backup to SQL file
   pg_dump -h localhost -U construbot_user construbot_dev > backup.sql

Restore Database
----------------

.. code-block:: bash

   # Drop existing database
   psql postgres -c "DROP DATABASE construbot_dev;"

   # Create fresh database
   psql postgres -c "CREATE DATABASE construbot_dev;"

   # Restore from backup
   psql -h localhost -U construbot_user construbot_dev < backup.sql

Reset Database
--------------

.. code-block:: bash

   # Drop and recreate
   psql postgres -c "DROP DATABASE construbot_dev;"
   psql postgres -c "CREATE DATABASE construbot_dev;"
   psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE construbot_dev TO construbot_user;"

   # Run migrations
   python manage.py migrate

   # Create superuser
   python manage.py createsuperuser

Access Database Console
------------------------

.. code-block:: bash

   # PostgreSQL console
   python manage.py dbshell

   # Or directly:
   psql -h localhost -U construbot_user -d construbot_dev

Troubleshooting
===============

Virtual Environment Issues
---------------------------

**Error:** "No module named 'django'"

**Cause:** Virtual environment not activated

**Solution:**

.. code-block:: bash

   source venv/bin/activate
   # Verify: which python should show path to venv

**Error:** "Command 'python' not found"

**Solution:** Use ``python3`` instead of ``python``

Database Connection Errors
---------------------------

**Error:** "could not connect to server"

**Solution 1:** Check PostgreSQL is running

.. code-block:: bash

   # macOS
   brew services list | grep postgresql

   # Linux
   sudo systemctl status postgresql

**Solution 2:** Verify DATABASE_URL in .env

.. code-block:: bash

   # Should match your database credentials
   DATABASE_URL=postgresql://construbot_user:construbot_pass@localhost:5432/construbot_dev

**Solution 3:** Check PostgreSQL is accepting connections

.. code-block:: bash

   psql -h localhost -U construbot_user -d construbot_dev

If this fails, check ``pg_hba.conf`` configuration.

Redis Connection Errors
------------------------

**Error:** "Error 111 connecting to localhost:6379"

**Solution:** Start Redis

.. code-block:: bash

   # macOS
   brew services start redis

   # Linux
   sudo systemctl start redis

   # Verify:
   redis-cli ping
   # Should respond: PONG

Permission Errors
-----------------

**Error:** "permission denied to create database"

**Solution:** Grant privileges to PostgreSQL user

.. code-block:: sql

   -- As PostgreSQL superuser
   GRANT ALL PRIVILEGES ON DATABASE construbot_dev TO construbot_user;
   ALTER USER construbot_user CREATEDB;

Migration Errors
----------------

**Error:** "No migrations to apply"

**Cause:** Migrations already applied

**Verify:**

.. code-block:: bash

   python manage.py showmigrations

**Error:** "Migration is applied before its dependency"

**Solution:** Reset migrations (WARNING: destroys data)

.. code-block:: bash

   # Drop database and start fresh
   # See "Reset Database" section above

Port Already in Use
-------------------

**Error:** "That port is already in use"

**Solution:** Find and kill process

.. code-block:: bash

   # macOS/Linux
   lsof -ti:8000 | xargs kill -9

   # Or use different port
   python manage.py runserver 8001

Development Tips
================

Auto-reload Not Working
-----------------------

Django's auto-reload should restart on code changes. If not:

.. code-block:: bash

   # Run with --noreload to disable (for debugging)
   python manage.py runserver --noreload

   # Check file watchers limit (Linux)
   cat /proc/sys/fs/inotify/max_user_watches

IDE Integration
---------------

**PyCharm:**

1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Existing environment
3. Select ``venv/bin/python``

**VS Code:**

1. Cmd+Shift+P → "Python: Select Interpreter"
2. Choose ``./venv/bin/python``

**.vscode/settings.json:**

.. code-block:: json

   {
     "python.pythonPath": "venv/bin/python",
     "python.linting.enabled": true,
     "python.linting.pylintEnabled": true,
     "python.formatting.provider": "black"
   }

Shell Aliases
-------------

Add to ``~/.bashrc`` or ``~/.zshrc``:

.. code-block:: bash

   # Construbot aliases
   alias cbot='cd ~/construbot && source venv/bin/activate'
   alias crun='python manage.py runserver'
   alias cmigrate='python manage.py migrate'
   alias cshell='python manage.py shell'

Then use:

.. code-block:: bash

   cbot     # Navigate and activate
   crun     # Run server
   cmigrate # Run migrations

Upgrading Dependencies
======================

Update Requirements Files
--------------------------

.. code-block:: bash

   # Install pip-tools
   pip install pip-tools

   # Update compiled requirements
   make pipcompile

   # Sync your environment
   pip-sync requirements/local.txt

Manual Upgrade
--------------

.. code-block:: bash

   # Update specific package
   pip install --upgrade django

   # Update all packages (be careful!)
   pip list --outdated
   pip install --upgrade <package-name>

   # Freeze new versions
   pip freeze > requirements/local.txt

After Upgrade
-------------

.. code-block:: bash

   # Run migrations
   python manage.py migrate

   # Run tests
   make localtest

   # Check for deprecation warnings
   python -Wd manage.py runserver

Next Steps
==========

After successful installation:

1. **Populate test data:** ``python manage.py poblar``
2. **Explore the codebase:** :doc:`../architecture/overview`
3. **Read API docs:** :doc:`../api/index`
4. **Check development workflow:** :doc:`/contributor/development-setup`

See Also
========

- :doc:`docker-setup` - Docker development setup (alternative)
- :doc:`requirements` - Understanding dependencies
- :doc:`configuration` - Environment variable reference
- :doc:`/contributor/testing/running-tests` - Testing guide
