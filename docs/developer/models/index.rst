======
Models
======

Data model documentation for Construbot.

Overview
========

Construbot's data models are organized into several apps:

- **users:** User, Company, Customer, NivelAcceso
- **proyectos:** Contrato, Contraparte, Sitio, Estimate, Concept, Retenciones
- **core:** Base models and utilities

Multi-Tenant Architecture
==========================

**All business models include:**

.. code-block:: python

   class BusinessModel(models.Model):
       company = models.ForeignKey(Company, on_delete=models.CASCADE)
       # ... other fields

See :doc:`../architecture/multi-tenancy` for details.

Key Models
==========

User Models (users app)
-----------------------

**Customer** - Top-level account

**Company** - Business entity (tenant)

**User** - Custom user model with email authentication

**NivelAcceso** - Permission levels (1-6)

See :doc:`users` for complete reference.

Business Models (proyectos app)
--------------------------------

**Contrato** - Contract/Project (hierarchical using django-treebeard)

**Contraparte** - Counterparty (Client, Subcontractor, Piecework Contractor)

**Sitio** - Construction site

**Estimate** - Progress payment/estimate

**Concept** - Line item in contract catalog

**Retenciones** - Financial retentions/withholdings

See :doc:`proyectos` for complete reference.

Model Relationships
===================

.. code-block:: text

   Customer
   └── Company
       ├── User (M2M)
       ├── Contrato
       │   ├── Contraparte (FK)
       │   ├── Sitio (FK)
       │   ├── Estimate (reverse FK)
       │   └── Concept (reverse FK)
       ├── Contraparte
       └── Sitio

Common Patterns
===============

**Company-scoped queries:**

.. code-block:: python

   # Always filter by company
   contracts = Contrato.objects.filter(company=request.user.active_company)

**Tree operations:**

.. code-block:: python

   # Hierarchical contracts
   children = contract.get_children()
   ancestors = contract.get_ancestors()
   descendants = contract.get_descendants()

**Unique per company:**

.. code-block:: python

   class Meta:
       unique_together = ('company', 'folio')

See Also
========

- :doc:`../architecture/database-schema` - Database design
- :doc:`../architecture/multi-tenancy` - Multi-tenant architecture
- :doc:`../api/index` - API reference
