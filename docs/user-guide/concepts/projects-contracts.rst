============================
Projects & Contracts
============================

.. note::
   **Spanish Term:** Contrato

   In Construbot, "Contrato" refers to both construction projects and contracts.
   The system supports hierarchical contracts (sub-contracts).

Overview
========

A **Contract** (Contrato) is the central entity in Construbot, representing a construction project or agreement.
Every aspect of work tracking, billing, and financial management revolves around contracts.

**Key Characteristics:**

- Hierarchical structure (parent/child relationships)
- Associated with a Counterparty (business partner)
- Linked to a construction Site (location)
- Contains a catalog of work items (Concepts)
- Tracks progress through Estimates
- Manages financial aspects (amount, advance, retentions)

What is a Contract?
===================

A contract in Construbot represents:

**Legal Agreement**
   The formal contract or agreement with a client, subcontractor, or piecework contractor.

**Project Container**
   A project that groups related work, estimates, and financial tracking.

**Financial Framework**
   Defines the total amount, advance payment, and retention rules.

**Work Catalog**
   Contains all work items (concepts) to be executed.

Contract Components
===================

Basic Information
-----------------

**Reference Number** (Folio)
   Sequential ID for contracts within your company (e.g., 1, 2, 3...).

**Contract Code** (Código)
   Your internal code matching the signed contract (e.g., "CONT-2024-001").

**Contract Name** (Nombre del contrato)
   Full descriptive name used in estimates and reports.

   *Example: "Downtown Office Tower - Complete Construction Phase 1"*

**Short Name** (Nombre corto)
   Abbreviated name for lists and navigation.

   *Example: "Office Tower P1"*

**Date** (Fecha)
   Contract signing or start date.

Relationships
-------------

**Counterparty** (Contraparte)
   The business partner for this contract. Must be one of:

   - **Client** (Cliente) - If you're performing work for them
   - **Subcontractor** (Subcontratista) - If they're performing specialized work for you
   - **Piecework Contractor** (Destajista) - If they're doing task-based work

**Site** (Sitio)
   The construction location where work will be performed.
   Must be associated with a Client counterparty.

**Users** (Usuarios)
   Team members assigned to this contract. Only assigned users can view/edit the contract.

Financial Fields
----------------

**Amount** (Monto)
   Total contract value, typically specified **without VAT/IVA**.

   *Example: $1,000,000.00*

**Advance Payment** (Anticipo)
   Percentage (0-100%) paid upfront by the client for mobilization.
   This amount will be amortized (recovered) across subsequent estimates.

   *Example: 10% = $100,000.00 advance on a $1,000,000 contract*

**Status** (Status)
   Boolean indicating if the project is **ongoing** (active) or **completed** (inactive).

Documents
---------

**Contract PDF** (PDF del Contrato)
   Upload the signed contract document for reference.

Hierarchical Structure
======================

One of Construbot's powerful features is **hierarchical contracts** using parent-child relationships.

Why Use Hierarchy?
------------------

**Separate Sub-Contractor Management**
   Track work by different subcontractors under a main contract:

   .. code-block:: text

      Main Building Contract ($1,000,000)
      ├── Electrical Sub-Contract ($150,000)
      ├── Plumbing Sub-Contract ($100,000)
      ├── HVAC Sub-Contract ($120,000)
      └── Interior Finishes Sub-Contract ($180,000)

**Consolidated Reporting**
   Generate reports that roll up totals from all sub-contracts to the parent.

**Different Teams**
   Assign different users to different sub-contracts while maintaining overall project visibility.

**Clear Financial Separation**
   Track costs and progress separately for each specialized area.

Creating Hierarchy
------------------

**Parent Contract:**
   Create a main contract using the standard "Create Contract" form.

**Child Contracts:**
   Use the "Create Sub-Contract" option and select the parent contract.

**Tree Operations:**

- Add multiple children to any parent
- Add children to children (multi-level hierarchy)
- Move contracts within the tree (with caution)

.. warning::
   **Deletion Rules**: You cannot delete a parent contract that has children.
   Delete all child contracts first.

Contract Lifecycle
==================

1. Creation
-----------

**Initial Setup:**

- Create or select Counterparty
- Create or select Site
- Define contract details (folio, name, amount, date)
- Set advance payment percentage
- Assign users
- Upload signed contract PDF (optional)

**Result:** Empty contract ready for work catalog.

2. Catalog Definition
----------------------

**Add Work Items (Concepts):**

- Manually enter each work item, OR
- Import from Excel spreadsheet

**Define Retentions:**

- Add percentage-based retentions (e.g., 5%)
- Add fixed-amount retentions (e.g., $10,000)

**Result:** Contract with complete work catalog and retention rules.

3. Execution
------------

**Track Progress:**

- Create periodic estimates (Estimaciones)
- Document completed quantities for each concept
- Generate PDF estimates
- Submit to client for approval

**Result:** Work progress documented, payments tracked.

4. Financial Management
-----------------------

**Payment Tracking:**

- Mark estimates as invoiced (facturada)
- Record when payments are received (pagada)
- Monitor outstanding amounts on dashboard

**Automatic Calculations:**

- Advance amortization across estimates
- Retention deductions
- Accumulated totals

**Result:** Clear financial visibility.

5. Completion
-------------

**Project Close:**

- Final estimate created
- All work completed
- Final payment received (including retained amounts)
- Contract status set to inactive

**Result:** Closed project with complete financial history.

Contract Types by Counterparty
===============================

Client Contracts
----------------

**When:** Your company is the contractor performing work.

**Counterparty Type:** Cliente (Client)

**Financial Flow:** Client pays you for completed work.

**Example:**
   *"Office Building Construction for ABC Corp"*

   - Counterparty: ABC Corp (Cliente)
   - Your role: General Contractor
   - Payment: You receive money

Subcontractor Contracts
-----------------------

**When:** You hire a specialized contractor for part of a project.

**Counterparty Type:** Subcontratista (Subcontractor)

**Financial Flow:** You pay the subcontractor for their work.

**Example:**
   *"Electrical Installation - Subcontracted to XYZ Electric"*

   - Counterparty: XYZ Electric (Subcontratista)
   - Your role: General Contractor hiring specialist
   - Payment: You pay money
   - Typically a **child contract** under a main client contract

Piecework Contracts
-------------------

**When:** You hire workers paid by completed units (piece rate).

**Counterparty Type:** Destajista (Piecework Contractor)

**Financial Flow:** You pay per completed task/quantity.

**Example:**
   *"Masonry Work - Paid per Square Meter"*

   - Counterparty: José García (Destajista)
   - Your role: General Contractor
   - Payment: You pay based on quantity (e.g., $50/m²)
   - Common in Mexican construction industry

Financial Calculations
======================

Understanding Contract Amounts
-------------------------------

**Total Contracted** (Importe Total Contratado)
   The ``monto`` field - total contract value.

**Accumulated Executed** (Ejercido Acumulado)
   Sum of all work billed across all estimates to date.
   Calculated by: ``ejercido_acumulado()`` method.

**Remaining** (Por Ejercer)
   Total Contracted minus Accumulated Executed.

**Example:**

.. code-block:: text

   Contract Amount:        $1,000,000.00

   Estimate #1:            $  200,000.00
   Estimate #2:            $  150,000.00
   Estimate #3:            $  180,000.00
   ─────────────────────────────────────
   Accumulated Executed:   $  530,000.00
   Remaining:              $  470,000.00

Advance Payment Mechanics
--------------------------

**Initial Advance:**
   If ``anticipo = 10%`` on a $1,000,000 contract:
   Client pays $100,000 upfront.

**Amortization:**
   The $100,000 is recovered across estimates until fully amortized.

**Example Amortization:**

.. list-table::
   :header-rows: 1
   :widths: 15 20 20 20 25

   * - Estimate
     - Work Value
     - Amortization
     - Net Payment
     - Remaining Advance
   * - #1
     - $200,000
     - $20,000 (10%)
     - $180,000
     - $80,000
   * - #2
     - $150,000
     - $15,000 (10%)
     - $135,000
     - $65,000
   * - #3
     - $180,000
     - $18,000 (10%)
     - $162,000
     - $47,000
   * - #4
     - $100,000
     - $10,000 (10%)
     - $90,000
     - $37,000
   * - #5
     - $120,000
     - $12,000 (10%)
     - $108,000
     - $25,000

The advance is recovered proportionally until the original $100,000 is fully amortized.

**Learn more:** :doc:`estimates`

Best Practices
==============

Naming Conventions
------------------

✅ **Good Contract Names:**
   - "Downtown Office Tower - Complete Construction Phase 1"
   - "Highway 101 Bridge - Structural Steel Installation"
   - "Residential Complex Unit A - Electrical Systems"

❌ **Avoid:**
   - "Project 1" (too generic)
   - "ABC" (unclear)
   - Just the contract code without description

Organize with Hierarchy
------------------------

✅ **Use sub-contracts for:**
   - Different subcontractors
   - Different phases of work
   - Different buildings/units in a complex

✅ **Keep main contract for:**
   - Overall client relationship
   - Consolidated reporting
   - Total project tracking

User Assignment
---------------

✅ **Assign users who need access:**
   - Project Manager (always)
   - Site Supervisor
   - Coordinators creating estimates
   - Accounting staff tracking payments

✅ **Permission levels:**
   - Director (Level 3+): Can create/edit contracts
   - Coordinador (Level 2): Can create estimates
   - Auxiliar (Level 1): View-only access

Keep Status Updated
-------------------

✅ **Active contracts:**
   - Set ``status = True`` (ongoing) for projects in progress
   - Appear in "Active Contracts" dashboard section

✅ **Completed contracts:**
   - Set ``status = False`` when project is finished
   - Removes from active list but retains all history

Common Scenarios
================

Scenario 1: Main Contract with Subcontractors
----------------------------------------------

**Setup:**

1. Create main client contract: "Office Building for ABC Corp" ($1,000,000)
2. Create sub-contracts as children:

   - "Electrical - XYZ Electric" ($150,000) - Subcontratista
   - "Plumbing - AAA Plumbing" ($100,000) - Subcontratista
   - "HVAC - Cool Systems" ($120,000) - Subcontratista

3. Track work separately for each sub-contract
4. Generate consolidated report for ABC Corp showing all work

**Benefit:** Clear separation of subcontractor costs while maintaining overall project view.

Scenario 2: Multi-Phase Project
--------------------------------

**Setup:**

1. Create parent: "Residential Complex - Master Contract"
2. Create children for each phase:

   - "Phase 1 - Foundation & Structure"
   - "Phase 2 - MEP & Finishes"
   - "Phase 3 - Landscaping & Exterior"

3. Execute phases sequentially or in parallel
4. Track financial progress per phase

**Benefit:** Clear phase separation with consolidated totals.

Scenario 3: Multiple Buildings
-------------------------------

**Setup:**

1. Create parent: "Shopping Center Development"
2. Create children for each building:

   - "Building A - Retail Spaces"
   - "Building B - Food Court"
   - "Building C - Parking Structure"

3. Assign different teams to different buildings
4. Track progress independently

**Benefit:** Independent management with overall project visibility.

Troubleshooting
===============

Can't Delete a Contract
-----------------------

**Problem:** "Cannot be deleted, has concepts that must be deleted first" or has child contracts.

**Solution:**

1. For concepts: Delete all work items (concepts) from the contract first
2. For children: Delete all sub-contracts first, then delete parent
3. Alternatively: Set contract to inactive instead of deleting

Can't See a Contract
--------------------

**Problem:** Contract doesn't appear in your list.

**Causes:**

- You're in the wrong **company** (use Switch Company)
- You're not **assigned** to the contract (contact admin)
- Your **permission level** is too low

Can't Edit Contract
-------------------

**Problem:** Edit option is disabled.

**Requirements:**

- Minimum **Director** (Level 3) permission
- Must be **assigned** to the contract
- Must be in the correct **company**

Retentions Not Showing
----------------------

**Problem:** Retentions not appearing in estimates.

**Solution:**

1. Navigate to Contract Detail
2. Click "Retentions" tab
3. Add retention rules (percentage or fixed amount)
4. Retentions will automatically apply to future estimates

See Also
========

**Related Concepts:**

- :doc:`counterparties` - Understanding business partners
- :doc:`estimates` - Tracking progress and payments
- :doc:`concepts-line-items` - Work items in contracts
- :doc:`retentions` - Financial withholdings
- :doc:`sites-contacts` - Locations and contacts

**Workflows:**

- :doc:`/user-guide/workflows/creating-project` - Complete project setup
- :doc:`/user-guide/workflows/subcontracts` - Working with hierarchies
- :doc:`/user-guide/workflows/managing-estimates` - Estimate creation

**Features:**

- :doc:`/user-guide/features/hierarchical-contracts` - Deep dive into hierarchy
- :doc:`/user-guide/features/multi-company` - Multi-tenant usage

**Developer Reference:**

- :doc:`/developer/models/proyectos` - Contrato model documentation
- :doc:`/developer/architecture/multi-tenancy` - System architecture
