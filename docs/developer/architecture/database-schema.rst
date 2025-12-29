===============
Database Schema
===============

Database design and relationships in Construbot.

Overview
========

**Database:** PostgreSQL 12+

**Key model groups:**

- **Users & Auth:** User, Company, Customer, NivelAcceso
- **Contracts:** Contrato (hierarchical), Contraparte, Sitio
- **Financials:** Estimate, Concept, Retenciones
- **Configuration:** Account settings, Units

Core Relationships
==================

Multi-Tenancy Structure
-----------------------

.. code-block:: text

   Customer (1)
   └── Company (N)
       └── User (N via M2M)

   All business data → Company (FK)

**Foreign keys:**

- Company → Customer
- User ↔ Company (ManyToMany through UserCompany)
- All business models → Company

Contract Hierarchy
------------------

.. code-block:: text

   Contrato (uses django-treebeard)
   ├── path (Materialized Path)
   ├── depth
   └── numchild

   Parent Contract
   ├── Subcontract 1
   │   └── Sub-subcontract 1.1
   └── Subcontract 2

**Tree operations:**

- ``get_children()``
- ``get_ancestors()``
- ``get_descendants()``
- ``move(target, pos)``

Contract Relationships
----------------------

.. code-block:: text

   Contrato
   ├── company (FK) → Company
   ├── contraparte (FK) → Contraparte
   ├── sitio_trabajo (FK) → Sitio
   ├── destinatario (FK) → Destinatario
   └── estimates (reverse FK) ← Estimate

Key Models Reference
====================

Users & Companies
-----------------

**Customer:**

.. code-block:: python

   class Customer(models.Model):
       nombre = CharField(max_length=200)
       slug = SlugField(unique=True)
       activo = BooleanField(default=True)

**Company:**

.. code-block:: python

   class Company(models.Model):
       customer = FK(Customer)
       nombre = CharField(max_length=200)
       slug = SlugField()
       # unique_together = ('customer', 'slug')

**User:**

.. code-block:: python

   class User(AbstractUser):
       email = EmailField(unique=True)  # USERNAME_FIELD
       companies = M2M(Company, through='UserCompany')
       active_company = FK(Company, null=True)
       nivel_acceso = FK(NivelAcceso)

Contracts & Counterparties
---------------------------

**Contrato:**

.. code-block:: python

   class Contrato(MP_Node):  # Materialized Path tree
       company = FK(Company)
       folio = CharField(max_length=100)
       contraparte = FK(Contraparte)
       monto = DecimalField(max_digits=20, decimal_places=2)
       anticipo = DecimalField(...)  # Advance payment
       # unique_together = ('company', 'folio')

**Contraparte:**

.. code-block:: python

   class Contraparte(models.Model):
       company = FK(Company)
       nombre = CharField(max_length=200)
       tipo = CharField(choices=TIPO_CONTRAPARTE)
       # TIPO: CLIENTE, DESTAJISTA, SUBCONTRATISTA

**Sitio:**

.. code-block:: python

   class Sitio(models.Model):
       company = FK(Company)
       cliente = FK(Contraparte, limit_choices_to={'tipo': 'CLIENTE'})
       nombre = CharField(max_length=200)
       direccion = TextField()

Estimates & Concepts
--------------------

**Estimate:**

.. code-block:: python

   class Estimate(models.Model):
       company = FK(Company)
       contrato = FK(Contrato)
       numero_estimacion = IntegerField()
       fecha = DateField()
       monto = DecimalField(...)

**Concept:**

.. code-block:: python

   class Concept(models.Model):
       company = FK(Company)
       contrato = FK(Contrato)
       code = CharField(max_length=50)
       descripcion = TextField()
       unidad = FK(Units)
       precio_unitario = DecimalField(...)
       cantidad = DecimalField(...)

Indexes & Constraints
=====================

Indexes
-------

**Common patterns:**

.. code-block:: python

   class Contrato(MP_Node):
       class Meta:
           indexes = [
               models.Index(fields=['company', 'folio']),
               models.Index(fields=['company', 'fecha_inicio']),
               models.Index(fields=['path']),  # Tree queries
           ]

Unique Constraints
------------------

**Company-scoped uniqueness:**

.. code-block:: python

   class Meta:
       unique_together = [
           ('company', 'folio'),  # Unique per company
       ]

Database Queries
================

Select Related
--------------

**Optimize foreign keys:**

.. code-block:: python

   # Avoid N+1
   contratos = Contrato.objects.select_related(
       'company',
       'contraparte',
       'sitio_trabajo'
   )

Prefetch Related
----------------

**Optimize reverse FK and M2M:**

.. code-block:: python

   users = User.objects.prefetch_related(
       'companies',
       'companies__customer'
   )

Tree Queries
------------

**Hierarchical data:**

.. code-block:: python

   # Get all descendants
   contract.get_descendants()

   # Get children only
   contract.get_children()

   # Get ancestors
   contract.get_ancestors()

Migrations
==========

**Key migrations:**

- Initial: Create all models
- django-treebeard: Add path/depth/numchild fields
- Company scoping: Add company FK to all models
- Unique constraints: Add unique_together

**Run migrations:**

.. code-block:: bash

   python manage.py makemigrations
   python manage.py migrate

Database Optimization
=====================

Connection Pooling
------------------

.. code-block:: python

   # In production settings
   DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes

Atomic Transactions
-------------------

.. code-block:: python

   # Enabled by default
   DATABASES['default']['ATOMIC_REQUESTS'] = True

Query Analysis
--------------

.. code-block:: python

   # Django Debug Toolbar shows queries
   # Or use django-silk for profiling

See Also
========

- :doc:`multi-tenancy` - Multi-tenant architecture
- :doc:`../models/index` - Model documentation
- :doc:`overview` - System architecture
