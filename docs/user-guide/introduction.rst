============
Introduction
============

What is Construbot?
===================

Construbot is a comprehensive operational management platform designed specifically for construction companies.
It provides tools to manage the complete lifecycle of construction projects, from initial contract setup through
final payment.

**Key Capabilities:**

- Contract and project management with hierarchical structure
- Progress billing and estimate tracking
- Financial calculations (retentions, advances, amortization)
- Multi-company and multi-user support
- Document generation and PDF exports
- Excel import for catalogs

Core Philosophy
===============

Construbot is built around construction industry best practices:

**Project-Centric**
   Everything revolves around Contracts (Contratos) - your construction projects.

**Financial Transparency**
   Clear tracking of amounts, payments, retentions, and advances.

**Hierarchical Organization**
   Support for main contracts with sub-contracts (destajistas, subcontratistas).

**Multi-Tenant**
   Work across multiple companies under a single customer account.

Who Uses Construbot?
====================

Construction Companies
----------------------

General contractors, builders, and construction firms who need to:

- Manage multiple simultaneous projects
- Track progress payments and estimates
- Handle subcontractor relationships
- Generate professional documentation

Project Teams
-------------

- **Directors**: Oversee multiple projects and financial summaries
- **Project Managers**: Manage day-to-day contract execution
- **Site Supervisors**: Track work progress and create estimates
- **Coordinators**: Handle document preparation and administration
- **Accounting Staff**: Process payments and invoicing

Key Features Overview
=====================

Contract Management
-------------------

Create and manage construction contracts (Contratos) with:

- Hierarchical structure (parent/child contracts)
- Associated business partners (Contrapartes)
- Construction sites (Sitios) and contacts (Destinatarios)
- Work item catalogs (Conceptos)

**Learn more:** :doc:`concepts/projects-contracts`

Progress Estimates
------------------

Track work completion with periodic estimates (Estimaciones):

- Document work quantities for each concept
- Calculate accumulated totals
- Apply retentions and advance amortization
- Mark estimates as invoiced and paid

**Learn more:** :doc:`concepts/estimates`

Financial Tracking
------------------

Automated calculations for:

- **Advance Payments** (Anticipos) - Initial down payments
- **Retentions** (Retenciones) - Withholdings (percentage or fixed amount)
- **Amortization** - Recovery of advance payments over time
- **Accumulated Totals** - Running totals across all estimates

**Learn more:** :doc:`workflows/managing-estimates`

Multi-Company Support
---------------------

Work across multiple business entities:

- Single login for multiple companies
- Easy company switching
- Data isolation between companies
- Role-based access control

**Learn more:** :doc:`features/multi-company`

Document Generation
-------------------

Generate professional PDFs:

- Contract estimates for client approval
- Progress payment documentation
- Hierarchical reports for sub-contracts
- Custom branding and formatting

**Learn more:** :doc:`workflows/document-generation`

System Architecture
===================

Understanding the Hierarchy
----------------------------

Construbot uses a three-level organizational structure:

.. code-block:: text

   Customer (Top Level Account)
   └── Company (Business Entity)
       └── User (Individual with permissions)

**Customer** (Cliente Sistema)
   Your top-level account. One customer can have multiple companies.

**Company** (Empresa)
   A business entity. Users can belong to multiple companies.

**User** (Usuario)
   Individual with email login and permission levels (1-6).

Permission Levels
-----------------

Users are assigned permission levels (Niveles de Acceso):

1. **Auxiliar** (Assistant) - View-only or limited access
2. **Coordinador** (Coordinator) - Create and edit documents
3. **Director** (Director) - Full project management
4. **Corporativo** (Corporate) - Cross-project oversight
5. **Soporte** (Support) - Technical support access
6. **Superusuario** (Superuser) - Full system access

**Learn more:** :doc:`/developer/architecture/permission-levels`

Spanish Terminology
===================

Construbot was developed in Mexico and uses Spanish terminology throughout the interface.
This documentation provides English translations for all terms.

**Common Terms:**

- **Contrato** = Contract / Project
- **Contraparte** = Counterparty / Business Partner
- **Estimación** = Estimate / Progress Payment
- **Concepto** = Concept / Line Item / Work Item
- **Sitio** = Site / Construction Location

**Full Glossary:** See :doc:`/reference/glossary` for complete translations.

Next Steps
==========

Ready to start? Continue to:

- :doc:`getting-started` - First steps with Construbot
- :doc:`concepts/index` - Understand core concepts
- :doc:`workflows/index` - Learn common workflows

.. tip::
   **For Developers**: If you're installing or deploying Construbot, see the
   :doc:`/developer/index` instead.
