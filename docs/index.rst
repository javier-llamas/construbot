===================================
Construbot Documentation
===================================

.. image:: https://img.shields.io/badge/Python-3.9.17%2B-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/Django-3.2.19-green.svg
   :target: https://www.djangoproject.com/
   :alt: Django Version

.. image:: https://img.shields.io/badge/license-AGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0.en.html
   :alt: License

**Una Solución Operativa para Constructoras** | An Operational Solution for Construction Companies

Construbot is a comprehensive Django-based construction management system for tracking contracts, estimates, counterparties, and financial operations. Built with multi-tenancy, hierarchical data structures, and a powerful REST API.

.. note::
   **Language Note:** While the codebase uses Spanish terminology (Contrato, Estimación, etc.), this documentation is primarily in English with Spanish translations available. See :doc:`_glossary/domain-terms` for complete term translations.

Quick Links
===========

.. grid:: 3
   :gutter: 3

   .. grid-item-card:: 📚 User Guide
      :link: user-guide/index
      :link-type: doc
      :class-card: sd-text-center

      **For End Users**

      Learn how to use Construbot for managing construction projects, contracts, and estimates.

      +++
      :doc:`Get Started → <user-guide/getting-started>`

   .. grid-item-card:: 🔧 Developer Docs
      :link: developer/index
      :link-type: doc
      :class-card: sd-text-center

      **For Developers**

      Installation, deployment, architecture, API reference, and technical documentation.

      +++
      :doc:`Install Now → <developer/installation/index>`

   .. grid-item-card:: 🤝 Contributor Guide
      :link: contributor/index
      :link-type: doc
      :class-card: sd-text-center

      **For Contributors**

      Testing, translation, code style, and contribution guidelines.

      +++
      :doc:`Contribute → <contributor/getting-started>`

What is Construbot?
===================

Construbot helps construction companies manage:

✅ **Hierarchical Contracts** - Parent contracts with subcontracts using tree structures

✅ **Progress Estimates** - Track work completion and payments (Estimaciones)

✅ **Counterparty Management** - Clients, subcontractors, and piecework contractors

✅ **Financial Tracking** - Advances, retentions, and payment calculations

✅ **Multi-Company Support** - One system for multiple business entities

✅ **PDF Generation** - Automated document creation

✅ **Excel Import/Export** - Bulk data operations

✅ **REST API** - Mobile and external integrations

Key Features
============

**Multi-Tenant Architecture**

Three-level hierarchy (Customer → Company → User) with complete data isolation between companies.

**Hierarchical Contracts**

Use django-treebeard for parent/child contract relationships with automatic financial aggregation.

**Email-Based Authentication**

Modern authentication using email (not usernames) with six permission levels from Auxiliar to Superusuario.

**Production-Ready**

Docker deployment, PostgreSQL database, Redis caching, Celery tasks, S3 storage, and comprehensive security.

Technology Stack
================

.. code-block:: text

   Backend Framework: Django 3.2.19 (Python 3.9.17+)
   Database: PostgreSQL 12+
   Cache/Queue: Redis 6+
   Task Queue: Celery 5.2.7
   API: Django REST Framework + SimpleJWT
   PDF Generation: ReportLab
   Tree Structures: django-treebeard

Quick Start
===========

**For Users:**

.. code-block:: bash

   # Access the application
   https://your-construbot-instance.com

   # Log in with your email and password
   # See: user-guide/getting-started

**For Developers (Docker):**

.. code-block:: bash

   # Clone repository
   git clone https://github.com/javier-llamas/construbot.git
   cd construbot

   # Build and start
   make buildev

   # Create superuser
   make superuser

   # Access at http://localhost:8000

See :doc:`developer/installation/index` for complete setup.

Documentation Structure
=======================

This documentation is organized for three audiences:

User Guide
----------

**For end users** managing construction projects:

- :doc:`user-guide/introduction` - What is Construbot
- :doc:`user-guide/getting-started` - First steps tutorial
- :doc:`user-guide/concepts/index` - Core concepts (contracts, estimates, etc.)
- :doc:`user-guide/workflows/index` - Step-by-step workflows
- :doc:`user-guide/features/index` - Advanced features
- :doc:`user-guide/faq` - Common questions

Developer Documentation
-----------------------

**For developers** installing or extending Construbot:

- :doc:`developer/installation/index` - Development setup
- :doc:`developer/deployment/index` - Production deployment
- :doc:`developer/architecture/index` - System architecture
- :doc:`developer/api/index` - REST API reference
- :doc:`developer/models/index` - Data models

Contributor Guide
-----------------

**For contributors** improving Construbot:

- :doc:`contributor/index` - Getting started
- :doc:`contributor/testing/index` - Testing guide
- :doc:`contributor/translation/glossary` - Translation glossary
- :doc:`contributor/documentation/index` - Documentation guidelines

Reference
---------

**Quick reference** for all users:

- :doc:`reference/glossary` - Spanish→English terms
- :doc:`reference/makefile-commands` - Development commands
- :doc:`_glossary/domain-terms` - Complete glossary

Popular Pages
=============

**Getting Started:**

- :doc:`user-guide/getting-started` - User tutorial
- :doc:`developer/installation/docker-setup` - Docker development
- :doc:`developer/deployment/aws-ec2` - AWS deployment

**Core Concepts:**

- :doc:`user-guide/concepts/projects-contracts` - Understanding contracts
- :doc:`developer/architecture/multi-tenancy` - Multi-tenant architecture
- :doc:`_glossary/domain-terms` - Complete Spanish→English glossary

**Configuration:**

- :doc:`developer/installation/configuration` - Environment variables
- :doc:`developer/deployment/environment-variables` - Production config
- :doc:`developer/architecture/settings-structure` - Django settings

Spanish Terminology
===================

The codebase uses Spanish business terminology. Key translations:

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Spanish
     - English
     - Description
   * - Contrato
     - Contract / Project
     - Main business entity
   * - Contraparte
     - Counterparty
     - Client, subcontractor, or contractor
   * - Estimación
     - Estimate / Progress Payment
     - Payment request for completed work
   * - Concepto
     - Concept / Line Item
     - Individual work item in catalog
   * - Retención
     - Retention / Withholding
     - Financial withholding
   * - Sitio
     - Site
     - Construction site location

See :doc:`_glossary/domain-terms` for **100+ complete translations**.

Repository & License
====================

**GitHub:** https://github.com/javier-llamas/construbot

**License:** GNU Affero General Public License v3 (AGPLv3)

**Current Version:** 1.1.04

Get Help
========

- **Installation Issues:** :doc:`developer/installation/index`
- **Deployment Problems:** :doc:`developer/deployment/index`
- **API Questions:** :doc:`developer/api/index`
- **Bug Reports:** https://github.com/javier-llamas/construbot/issues

Documentation Sections
======================

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :hidden:

   user-guide/index
   user-guide/introduction
   user-guide/getting-started
   user-guide/concepts/index
   user-guide/workflows/index
   user-guide/features/index
   user-guide/faq

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation
   :hidden:

   developer/index
   developer/installation/index
   developer/deployment/index
   developer/architecture/index

.. toctree::
   :maxdepth: 2
   :caption: Contributor Guide
   :hidden:

   contributor/index

.. toctree::
   :maxdepth: 2
   :caption: Reference
   :hidden:

   reference/glossary
   reference/makefile-commands
   _glossary/domain-terms

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
