==============
Core Concepts
==============

Understanding Construbot's core concepts is essential for effectively managing your construction projects.
This section explains the key entities and how they relate to each other.

.. note::
   **Spanish Terms**: Construbot uses Spanish terminology. Each concept includes the Spanish term
   for reference. See :doc:`/reference/glossary` for complete translations.

Overview
========

Construbot organizes construction management around these core entities:

.. image:: /_static/images/entity-relationships.png
   :alt: Entity Relationships
   :align: center

*(Diagram placeholder showing relationships between entities)*

Key Entities
============

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 🏗️ Projects & Contracts
      :link: projects-contracts
      :link-type: doc

      **Contrato** - The central entity representing construction projects and contracts.

   .. grid-item-card:: 🤝 Counterparties
      :link: counterparties
      :link-type: doc

      **Contraparte** - Business partners: Clients, Subcontractors, and Piecework Contractors.

   .. grid-item-card:: 📊 Estimates
      :link: estimates
      :link-type: doc

      **Estimación** - Progress payments and billing for completed work.

   .. grid-item-card:: 📝 Concepts & Line Items
      :link: concepts-line-items
      :link-type: doc

      **Concepto** - Individual work items in a contract catalog.

   .. grid-item-card:: 📍 Sites & Contacts
      :link: sites-contacts
      :link-type: doc

      **Sitio & Destinatario** - Construction locations and contact persons.

   .. grid-item-card:: 💰 Retentions
      :link: retentions
      :link-type: doc

      **Retención** - Financial withholdings and holdbacks.

Entity Relationships
====================

Understanding how entities connect:

Contracts
---------

A **Contract** (Contrato) is linked to:

- **Counterparty** (Contraparte) - Who you have the contract with
- **Site** (Sitio) - Where the work happens
- **Concepts** (Conceptos) - What work will be done
- **Estimates** (Estimaciones) - Progress billing
- **Users** - Who manages the contract

Counterparties
--------------

A **Counterparty** (Contraparte) can have:

- **Sites** (Sitios) - Multiple locations (for Clients only)
- **Contacts** (Destinatarios) - People at the organization
- **Contracts** (Contratos) - Multiple projects

Estimates
---------

An **Estimate** (Estimación) links:

- **Contract** (Contrato) - Which project it belongs to
- **Estimate Concepts** - Quantities completed for each work item
- **Users** - Who drafted, supervised, and authorized it

Data Hierarchy
==============

Organizational Structure
------------------------

.. code-block:: text

   Customer (Cliente Sistema)
   └── Company (Empresa)
       ├── Users (Usuarios)
       ├── Counterparties (Contrapartes)
       │   ├── Sites (Sitios)
       │   └── Contacts (Destinatarios)
       ├── Contracts (Contratos)
       │   ├── Concepts (Conceptos)
       │   ├── Retentions (Retenciones)
       │   ├── Estimates (Estimaciones)
       │   └── Sub-Contracts (child Contratos)
       └── Units (Unidades)

Everything is scoped to a **Company** for multi-tenancy support.

Contract Hierarchy
------------------

Contracts can be hierarchical:

.. code-block:: text

   Main Contract (Parent)
   ├── Electrical Sub-Contract (Child)
   ├── Plumbing Sub-Contract (Child)
   └── HVAC Sub-Contract (Child)

This allows tracking of subcontractor work separately while rolling up totals to the parent.

**Learn more:** :doc:`projects-contracts`

Financial Flow
==============

Understanding the financial lifecycle:

1. **Contract Created**

   - Total amount (monto) defined
   - Advance payment % (anticipo) specified
   - Retentions (retenciones) configured

2. **Advance Payment**

   - Client pays initial percentage (e.g., 10%)
   - Funds mobilization and initial costs

3. **Work Completed**

   - Progress is tracked
   - Estimates document completed work

4. **Estimate Created**

   - Quantities for each concept recorded
   - System calculates:

     - Subtotal for completed work
     - Minus: Advance amortization (recovery of advance)
     - Minus: Retentions (withholdings)
     - Equals: Net payment due

5. **Invoicing & Payment**

   - Estimate marked as invoiced (facturada)
   - Payment received
   - Estimate marked as paid (pagada)

6. **Final Payment**

   - All work completed
   - Retained amounts released
   - Contract closed

**Learn more:** :doc:`estimates`, :doc:`retentions`

Common Workflows
================

The typical workflow combines these concepts:

**Project Setup**

1. Create Client (Contraparte - Cliente)
2. Create Site (Sitio)
3. Create Contacts (Destinatarios)
4. Create Contract (Contrato)
5. Add Work Items (Conceptos)
6. Configure Retentions (Retenciones)

**Execution**

1. Complete work on site
2. Create Estimate (Estimación)
3. Document quantities for each Concept
4. Generate PDF
5. Submit to client

**Financial Tracking**

1. Mark estimate as Invoiced
2. Receive payment
3. Mark estimate as Paid
4. Monitor dashboard for outstanding amounts

Terminology Quick Reference
============================

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Spanish Term
     - English Translation
     - Description
   * - Contrato
     - Contract / Project
     - Main construction project
   * - Contraparte
     - Counterparty
     - Business partner
   * - Cliente
     - Client
     - Customer paying for work
   * - Destajista
     - Piecework Contractor
     - Worker paid by task
   * - Subcontratista
     - Subcontractor
     - Specialized contractor
   * - Sitio
     - Site
     - Construction location
   * - Destinatario
     - Contact / Recipient
     - Person at organization
   * - Estimación
     - Estimate
     - Progress payment
   * - Concepto
     - Concept / Line Item
     - Work item
   * - Retención
     - Retention
     - Withholding
   * - Anticipo
     - Advance
     - Down payment
   * - Monto
     - Amount
     - Total value

**Full glossary:** :doc:`/reference/glossary`

Detailed Concepts
=================

.. toctree::
   :maxdepth: 1

   projects-contracts
   counterparties
   estimates
   sites-contacts
   retentions
   concepts-line-items

Next Steps
==========

- **Understand each concept** by reading the detailed pages
- **Learn workflows** in :doc:`/user-guide/workflows/index`
- **Explore features** in :doc:`/user-guide/features/index`

.. tip::
   Start with :doc:`projects-contracts` as it's the central entity in Construbot.
