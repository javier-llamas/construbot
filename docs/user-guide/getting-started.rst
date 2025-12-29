===============
Getting Started
===============

This guide will help you get started with Construbot, from your first login to creating your first project.

First Login
===========

1. **Navigate** to your Construbot instance URL
2. **Click** "Login" or navigate to ``/accounts/login``
3. **Enter** your email and password
4. **Click** "Sign In"

.. note::
   Construbot uses **email-based authentication**. Your username is your email address.

The Dashboard
=============

After login, you'll see the **Project Dashboard** (``/proyectos/``):

.. image:: /_static/images/dashboard.png
   :alt: Construbot Dashboard
   :align: center

*(Image placeholder - screenshot of main dashboard)*

Dashboard Sections
------------------

**Active Contracts**
   Lists all ongoing projects (Contratos) with progress percentages and financial summaries.

**Pending Invoicing**
   Estimates (Estimaciones) that have been completed but not yet invoiced.

**Pending Payment**
   Estimates that have been invoiced but payment hasn't been received.

**Quick Stats**
   Total amounts for unbilled and unpaid estimates.

Navigation Menu
===============

The main navigation provides access to:

Contracts (Contratos)
---------------------

- **List Contracts** - View all projects
- **Create Contract** - Start a new project
- **Create Sub-Contract** - Add child contract under existing project

Business Partners (Contrapartes)
---------------------------------

- **Clients** (Clientes) - Customers paying for work
- **Subcontractors** (Subcontratistas) - Specialized contractors
- **Piecework Contractors** (Destajistas) - Task-based workers

Locations & Contacts
--------------------

- **Sites** (Sitios) - Construction locations
- **Contacts** (Destinatarios) - People at partner organizations
- **Units** (Unidades) - Measurement units (m², kg, pza, etc.)

Your First Project
==================

Let's create your first contract step-by-step.

Step 1: Create a Client
------------------------

Before creating a contract, you need a client (Cliente):

1. Navigate to **Clients** menu
2. Click **"Create New Client"** (Nuevo Cliente)
3. Fill in the form:

   - **Client Name** (Nombre del cliente): Company or individual name
   - **Type** (Tipo): Select "CLIENTE"

4. Click **"Save"**

**Example:**
   - Name: "ABC Development Corporation"
   - Type: CLIENTE

Step 2: Create a Site
----------------------

Add the construction location:

1. Navigate to **Sites** menu (Sitios/Ubicaciones)
2. Click **"Create New Site"** (Nuevo Sitio)
3. Fill in:

   - **Site Name** (Nombre del sitio): Project location name
   - **Location** (Ubicación): Physical address or description
   - **Client** (Cliente): Select the client you just created

4. Click **"Save"**

**Example:**
   - Name: "Downtown Office Tower"
   - Location: "123 Main Street, Mexico City"
   - Client: ABC Development Corporation

Step 3: Create the Contract
----------------------------

Now create the main contract:

1. Navigate to **Contracts** menu
2. Click **"Create New Contract"** (Nuevo Contrato)
3. Fill in the form:

   **Basic Information:**

   - **Reference Number** (Folio): Sequential ID (e.g., 1)
   - **Contract Code** (Código): Your internal code (e.g., "CONT-2024-001")
   - **Contract Date** (Fecha): Signing date
   - **Contract Name** (Nombre del contrato): Full project name
   - **Short Name** (Nombre corto): Abbreviated name for listings

   **Relationships:**

   - **Counterparty** (Contraparte): Select your client
   - **Site** (Sitio): Select the construction site

   **Financial:**

   - **Amount** (Monto): Total contract value (without VAT)
   - **Advance %** (Anticipo): Down payment percentage (0-100)

   **Users:**

   - **Assigned Users** (Usuarios): Select team members

   **Status:**

   - **Ongoing** (Status): Check if project is active

4. Click **"Save"**

**Example:**
   - Folio: 1
   - Code: CONT-2024-001
   - Name: "Downtown Office Tower - Phase 1"
   - Short Name: "Office Tower P1"
   - Counterparty: ABC Development Corporation
   - Site: Downtown Office Tower
   - Amount: 1,000,000.00
   - Advance: 10% (10.00)

Step 4: Add Work Items (Concepts)
----------------------------------

Add the catalog of work items to your contract:

1. Navigate to your **Contract Detail** page
2. Click **"Concept Catalog"** tab
3. **Option A - Manual Entry:**

   - Click **"Add Concept"**
   - Fill in:

     - **Code**: Item code (e.g., "CONC-001")
     - **Description** (Concepto): Work description
     - **Unit** (Unidad): Select measurement unit (m², kg, pza)
     - **Quantity** (Cantidad): Total contracted quantity
     - **Unit Price** (Precio Unitario): Price per unit

   - Click **"Save"**

4. **Option B - Excel Import:**

   - Prepare Excel file with columns: Code, Description, Unit, Quantity, Unit Price
   - Click **"Import from Excel"**
   - Upload file
   - Review and confirm import

**Example Concepts:**

.. list-table::
   :header-rows: 1
   :widths: 15 35 15 15 20

   * - Code
     - Description
     - Unit
     - Quantity
     - Unit Price
   * - CONC-001
     - Concrete Foundation
     - m³
     - 500
     - $150.00
   * - CONC-002
     - Steel Framing
     - ton
     - 25
     - $2,500.00
   * - CONC-003
     - Electrical Installation
     - m
     - 1000
     - $25.00

Step 5: Create Your First Estimate
-----------------------------------

Track work progress with an estimate:

1. From **Contract Detail**, click **"Create Estimate"**
2. Fill in the estimate form:

   - **Estimate Number** (Consecutivo): Sequential number (e.g., 1)
   - **Start Date** (Fecha de inicio): Period start
   - **End Date** (Fecha de finalización): Period end
   - **Supervised By** (Supervisado por): Site supervisor
   - **Authorized By** (Autorizado por): Client representative(s)

3. **Add Quantities:**

   For each concept, enter:

   - **Quantity Estimated** (Cantidad estimada): Work completed this period
   - **Observations** (Observaciones): Optional notes

4. Click **"Save"**

**Example:**
   - Estimate #: 1
   - Period: March 1-31, 2024
   - Supervised By: John Doe
   - Quantities:

     - CONC-001: 100 m³ completed
     - CONC-002: 5 ton installed

.. tip::
   The system automatically calculates:

   - Subtotals per concept
   - Accumulated totals across estimates
   - Advance amortization
   - Retention deductions
   - Final payment amount

Step 6: Generate PDF
---------------------

Create a professional estimate document:

1. From **Estimate Detail**, click **"Generate PDF"**
2. Review the document
3. **Download** or **Print** as needed
4. Send to client for approval

Common Tasks
============

Switching Companies
-------------------

If you work for multiple companies:

1. Click your **username** in top navigation
2. Select **"Switch Company"**
3. Choose the company you want to work in
4. All data will now be filtered to that company

Marking Estimates as Invoiced
------------------------------

After sending invoice to client:

1. Open the **Estimate Detail**
2. Check **"Invoiced"** (Facturada) checkbox
3. Click **"Save"**

Marking Estimates as Paid
--------------------------

After receiving payment:

1. Open the **Estimate Detail**
2. Check **"Paid"** (Pagada) checkbox
3. Enter **"Payment Date"** (Fecha de pago)
4. Click **"Save"**

The estimate will be removed from "Pending Payment" on your dashboard.

Viewing Reports
---------------

**Sub-Contract Reports:**

For hierarchical contracts with sub-contracts:

1. Navigate to **Contract Detail** (parent contract)
2. Click **"Sub-Contract Report"**
3. View accumulated totals across all child contracts

**Dashboard Summaries:**

The dashboard automatically shows:

- Active contracts with progress %
- Financial totals (billed, unbilled, paid, unpaid)
- Contracts needing attention

Next Steps
==========

Now that you understand the basics:

- **Learn Core Concepts**: :doc:`concepts/index`
- **Master Workflows**: :doc:`workflows/index`
- **Explore Features**: :doc:`features/index`

.. tip::
   **Need the Spanish term for something?** Check the :doc:`/reference/glossary` for
   complete Spanish-English translations.

Troubleshooting
===============

Can't See a Contract?
---------------------

Make sure:

- You're in the correct **company** (use Switch Company)
- You're **assigned** to the contract (check with Director/Superuser)
- Your **permission level** allows access

Can't Create Estimates?
------------------------

Verify:

- Contract has **concepts** (work items) defined
- You have at least **Coordinador** (Level 2) permissions
- Contract **status** is active (ongoing)

Where Are My Retentions?
-------------------------

Retentions (Retenciones) are configured at the **contract level**:

1. Open **Contract Detail**
2. Click **"Retentions"** tab
3. Add retention rules (percentage or fixed amount)
4. Retentions will be automatically applied to estimates

.. seealso::

   - :doc:`concepts/retentions` - Understanding retention calculations
   - :doc:`workflows/creating-project` - Detailed project creation workflow
   - :doc:`faq` - Frequently Asked Questions
