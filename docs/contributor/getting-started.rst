===============
Getting Started
===============

First steps for contributing to Construbot.

Prerequisites
=============

**Required:**

- Git
- Python 3.9.17+
- Docker and Docker Compose (recommended)

**Or for local development:**

- PostgreSQL 12+
- Redis 6+
- Virtual environment

Fork and Clone
==============

**1. Fork repository:**

Visit https://github.com/javier-llamas/construbot and click "Fork"

**2. Clone your fork:**

.. code-block:: bash

   git clone https://github.com/YOUR-USERNAME/construbot.git
   cd construbot

**3. Add upstream remote:**

.. code-block:: bash

   git remote add upstream https://github.com/javier-llamas/construbot.git

Development Setup
=================

**Using Docker (Recommended):**

.. code-block:: bash

   # Build and start
   make buildev

   # Create superuser
   make superuser

   # Run tests
   make test

**Using Local Environment:**

.. code-block:: bash

   # Create virtualenv
   python3.9 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements/local.txt

   # Setup database
   python manage.py migrate

   # Run tests
   pytest

Making Changes
==============

**1. Create feature branch:**

.. code-block:: bash

   git checkout -b feature/my-feature

**2. Make changes**

**3. Run tests:**

.. code-block:: bash

   make test

**4. Commit:**

.. code-block:: bash

   git add .
   git commit -m "Add my feature"

**5. Push:**

.. code-block:: bash

   git push origin feature/my-feature

**6. Create Pull Request on GitHub**

Code Style
==========

**Format code:**

.. code-block:: bash

   # Black
   black .

   # isort
   isort .

**Lint:**

.. code-block:: bash

   pylint construbot/

See :doc:`code-style` for complete guidelines.

See Also
========

- :doc:`index` - Contributor guide home
- :doc:`testing/index` - Testing guide
- :doc:`/developer/installation/index` - Development setup
