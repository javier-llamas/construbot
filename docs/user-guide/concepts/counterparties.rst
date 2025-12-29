==============
Counterparties
==============

.. note::
   **Spanish Term:** Contraparte

Understanding counterparties (business partners) in Construbot.

.. contents:: Table of Contents
   :local:
   :depth: 2

What is a Counterparty?
=======================

A **Counterparty** (Spanish: **Contraparte**) is any business entity you work with on construction projects. This includes:

- **Clients** who hire your company
- **Subcontractors** who perform specialized work
- **Piecework Contractors** who are paid by completed work

**Model:** ``construbot.proyectos.models.Contraparte``

..
   SCREENSHOT RECOMMENDED: Counterparty list view showing different types

Types of Counterparties
========================

Construbot supports three types of counterparties:

1. Cliente (Client)
-------------------

**Who they are:**

- Organizations or individuals who hire your company
- The entity paying for the project
- The contract owner

**Use for:**

- Main construction contracts
- Service agreements
- Project owners

**Example:** "Acme Corporation hires your company to build a new office building"

..
   SCREENSHOT RECOMMENDED: Client counterparty creation form

2. Subcontratista (Subcontractor)
----------------------------------

**Who they are:**

- Specialized contractors performing specific work
- Hired by your company for projects
- Provide specialized services (electrical, plumbing, etc.)

**Use for:**

- Electrical work contracts
- Plumbing subcontracts
- HVAC installations
- Any specialized trade work

**Example:** "Your company hires an electrical contractor for building wiring"

..
   SCREENSHOT RECOMMENDED: Subcontractor counterparty details page

3. Destajista (Piecework Contractor)
-------------------------------------

**Who they are:**

- Contractors paid by completed work units
- Not hourly or salaried
- Compensation based on quantity completed

**Use for:**

- Construction work paid by square meter
- Installations paid per unit
- Any work compensated by output

**Example:** "Mason paid $50 per square meter of wall built"

..
   SCREENSHOT RECOMMENDED: Piecework contractor with unit-based pricing

Counterparty Information
=========================

Each counterparty record includes:

Basic Information
-----------------

**Required fields:**

- **Name** (nombre) - Company or individual name
- **Type** (tipo) - Cliente, Subcontratista, or Destajista
- **Company** - Your company (for multi-tenant isolation)

**Optional fields:**

- **RFC** - Tax ID number (Mexico)
- **Address** (dirección)
- **Phone** (teléfono)
- **Email**
- **Contact person** (persona de contacto)
- **Notes** (notas)

..
   SCREENSHOT RECOMMENDED: Complete counterparty form showing all fields

Creating a Counterparty
========================

Step 1: Access Counterparty List
---------------------------------

1. Log in to Construbot
2. Navigate to **Proyectos → Contrapartes**
3. Click **"New Counterparty"** or **"Agregar Contraparte"**

..
   SCREENSHOT RECOMMENDED: Counterparty list view with "New" button highlighted

Step 2: Fill Basic Information
-------------------------------

.. code-block:: text

   Name: Acme Construction Inc.
   Type: Cliente (Client)
   RFC: ACM950101ABC
   Address: 123 Construction Ave, Mexico City

Step 3: Add Contact Details
----------------------------

.. code-block:: text

   Phone: +52 55 1234 5678
   Email: contact@acmeconstruction.com
   Contact Person: John Smith, Project Manager

Step 4: Save
------------

Click **"Save"** or **"Guardar"** to create the counterparty.

Using Counterparties
=====================

In Contracts
------------

When creating a contract (Contrato):

1. Select counterparty from dropdown
2. Dropdown filtered by:
   - Your active company
   - Active counterparties only
   - Appropriate type for contract

**Example:**

- **Client contracts:** Only "Cliente" type available
- **Subcontracts:** Only "Subcontratista" and "Destajista"

..
   SCREENSHOT RECOMMENDED: Contract creation form with counterparty dropdown expanded

In Sites
--------

Sites (Sitios) are linked to **Client** counterparties:

1. Each site belongs to a specific client
2. Multiple sites per client allowed
3. Sites used for contract location

See :doc:`sites-contacts` for details.

Best Practices
==============

**1. Use descriptive names:**

.. code-block:: text

   GOOD: "ABC Electrical Services - Commercial Division"
   BAD: "ABC"

**2. Keep contact information current:**

Update phone and email when changes occur.

**3. One counterparty per legal entity:**

Don't create duplicates for different contacts at same company.

**4. Use appropriate type:**

- Cliente: When they're paying you
- Subcontratista: When you're paying them for specialized work
- Destajista: When payment is unit-based

**5. Deactivate instead of delete:**

Preserves historical data and relationships.

Common Scenarios
================

Scenario 1: Client with Multiple Sites
---------------------------------------

**Setup:**

1. Create one "Cliente" counterparty for the client
2. Create multiple sites under that client
3. Create contracts associated with different sites

**Example:**

- Client: "National Retail Corp"
- Sites: "Store #101 - Dallas", "Store #102 - Houston"
- Contracts: One contract per store

Scenario 2: Regular Subcontractor
----------------------------------

**Setup:**

1. Create "Subcontratista" counterparty
2. Mark as active
3. Reuse for multiple projects

Troubleshooting
===============

**Can't find counterparty in dropdown:**

- Check counterparty is marked "Active"
- Verify counterparty type matches contract type
- Confirm counterparty belongs to your active company

**Can't delete counterparty:**

Counterparties with contracts cannot be deleted. Instead:

1. Mark as inactive
2. Add note explaining why retired

See Also
========

- :doc:`projects-contracts` - Creating contracts with counterparties
- :doc:`sites-contacts` - Sites linked to client counterparties
- :doc:`/_glossary/domain-terms` - Complete terminology
