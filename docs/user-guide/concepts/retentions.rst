==========
Retentions
==========

.. note::
   **Spanish Term:** Retención

Understanding retentions (financial withholdings) in Construbot.

.. contents:: Table of Contents
   :local:
   :depth: 2

What is a Retention?
====================

A **Retention** (Spanish: **Retención**) is a percentage of payment withheld from estimates or invoices. Retentions serve as:

- Financial guarantee for contract completion
- Quality assurance holdback
- Warranty or defect correction fund
- Performance bond substitute
- Tax withholdings (in some jurisdictions)

**Model:** ``construbot.proyectos.models.Retenciones``

**Key Concept:** Retentions are deducted from estimate payments and held until specific conditions are met (contract completion, warranty period expiration, etc.).

..
   SCREENSHOT RECOMMENDED: Retention configuration on contract showing multiple retention types

How Retentions Work
===================

Basic Mechanism
---------------

When an estimate is created:

1. **Subtotal calculated** from line items
2. **Retention percentage applied** to subtotal
3. **Retention amount withheld** from payment
4. **Net payment** = Subtotal - Retention

**Example:**

.. code-block:: text

   Estimate Subtotal: $100,000
   Retention (10%): -$10,000
   Net Payment: $90,000

   Amount Withheld: $10,000 (held until release condition met)

Multiple Retentions
-------------------

Contracts can have multiple retention types applied simultaneously:

.. code-block:: text

   Estimate Subtotal: $100,000

   Retention 1 (Warranty - 5%): -$5,000
   Retention 2 (Performance - 3%): -$3,000
   Retention 3 (Tax Withholding - 2%): -$2,000

   Total Retentions: -$10,000
   Net Payment: $90,000

Each retention may have different release conditions and timing.

Retention Information
=====================

**Required fields:**

- **Name** (nombre) - Descriptive name
- **Percentage** (porcentaje) - Percentage to withhold (e.g., 10.00)
- **Contract** (contrato) - Which contract this applies to
- **Company** - Your company (for multi-tenant isolation)

**Optional fields:**

- **Description** (descripción) - Purpose and release conditions
- **Release Date** (fecha_liberacion) - When retention will be released
- **Released** (liberado) - Boolean flag if already released
- **Notes** (notas) - Additional information

..
   SCREENSHOT RECOMMENDED: Retention detail form showing all fields

Types of Retentions
===================

1. Performance Retentions
-------------------------

**Purpose:** Ensure contract completion according to specifications

**Typical Percentage:** 5-10%

**Release Condition:**

- Contract completion
- Final inspection approval
- Punch list items completed

**Example:**

.. code-block:: text

   Name: Performance Guarantee
   Percentage: 10%
   Description: Released upon final acceptance
   Release: Contract completion + 30 days

2. Warranty Retentions
----------------------

**Purpose:** Cover defect repairs during warranty period

**Typical Percentage:** 5%

**Release Condition:**

- Warranty period expiration (often 1 year)
- No outstanding defects
- Final sign-off from client

**Example:**

.. code-block:: text

   Name: Warranty Holdback
   Percentage: 5%
   Description: 12-month warranty coverage
   Release: 1 year after substantial completion

3. Tax Withholdings
-------------------

**Purpose:** Government-mandated tax collection

**Typical Percentage:** Varies by jurisdiction (1-10%)

**Release Condition:**

- Remitted to tax authority
- Not returned to contractor
- May be creditable against tax liability

**Example (Mexico):**

.. code-block:: text

   Name: IVA Retention
   Percentage: 2/3 of IVA (approximately 10.67%)
   Description: VAT withholding per Mexican tax law
   Release: Remitted to SAT monthly

4. Material/Labor Retentions
-----------------------------

**Purpose:** Ensure subcontractor or supplier payment

**Typical Percentage:** 5-10%

**Release Condition:**

- Proof of payment to subs/suppliers
- Lien waivers received
- No outstanding claims

Creating Retentions
===================

Method 1: Manual Creation
-------------------------

Step 1: Access Contract Retentions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Navigate to the contract
2. Find **"Retentions"** or **"Retenciones"** section
3. Click **"Add Retention"** or **"Agregar Retención"**

Step 2: Configure Retention
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Name: Performance Guarantee
   Percentage: 10.00
   Description: Released upon contract completion and final inspection
   Release Date: (leave blank until known)

Step 3: Save
^^^^^^^^^^^^^

Click **"Save"** to add this retention to the contract.

**Result:** This retention will automatically apply to all future estimates for this contract.

Method 2: Excel Import
----------------------

For contracts with standard retention structures:

1. Prepare Excel file with retention data:

.. code-block:: text

   Name, Percentage, Description
   Performance Guarantee, 10.00, Released upon completion
   Warranty Holdback, 5.00, Released after 1-year warranty

2. Navigate to contract retentions section
3. Click **"Import from Excel"**
4. Select file and upload

**Benefit:** Quickly set up multiple retentions at once.

..
   SCREENSHOT RECOMMENDED: Retention import interface showing Excel template and upload button

Retention Tracking
==================

Cumulative Retention Balance
-----------------------------

Construbot automatically tracks:

- **Total Retained This Estimate:** Sum of all retention amounts
- **Cumulative Retained:** Running total of all retained amounts
- **Released Amounts:** Retentions that have been paid out
- **Current Balance:** Total retained - Total released

**Example Tracking:**

.. code-block:: text

   Estimate #1: $10,000 retained
   Estimate #2: $8,000 retained
   Estimate #3: $12,000 retained
   Cumulative Retained: $30,000

   Retention Release (at completion): -$30,000
   Current Balance: $0

..
   SCREENSHOT RECOMMENDED: Retention tracking report showing cumulative balance and releases

Estimate-Level Retention Display
---------------------------------

Each estimate shows:

- Subtotal before retentions
- Each retention type and amount
- Total retentions
- Net amount to pay

**Estimate Example:**

.. code-block:: text

   Estimate #5 - January 2024

   Line Items Subtotal: $50,000

   Retentions:
   - Performance (10%): -$5,000
   - Warranty (5%): -$2,500
   Total Retentions: -$7,500

   Net Payment: $42,500

Releasing Retentions
====================

When to Release
---------------

Release retentions when conditions are met:

1. **Contract Completion:**
   - All work completed
   - Final inspection passed
   - Punch list items resolved

2. **Warranty Expiration:**
   - Warranty period ended
   - No outstanding defects
   - Client sign-off received

3. **Partial Releases:**
   - Milestone achievements
   - Progressive completion
   - Phase-based releases

Release Process
---------------

Step 1: Verify Release Conditions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Confirm all requirements met:

- Completion certificates obtained
- Client approval documented
- No outstanding claims or defects
- All required documentation submitted

Step 2: Mark Retention as Released
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Navigate to contract retention
2. Edit the retention record
3. Check **"Released"** flag
4. Enter **Release Date**
5. Add notes documenting release justification

Step 3: Generate Release Payment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Option A: Create Final Estimate**

Create a special estimate with:

- No new line items
- Negative retention amounts (to reverse withheld funds)
- Notes: "Retention Release - Contract Completion"

**Option B: Separate Payment Record**

Record retention release as separate transaction outside estimate system.

..
   SCREENSHOT RECOMMENDED: Retention release form with "Released" checkbox and release date field

Partial Retention Releases
---------------------------

For progressive releases:

**Scenario:** 50% of retention released at substantial completion, 50% after warranty

1. **Create two separate retentions:**

.. code-block:: text

   Retention 1: Performance - Substantial Completion (5%)
   Retention 2: Performance - Final Completion (5%)

2. **Release independently:**

- Release Retention 1 at substantial completion
- Release Retention 2 after warranty period

**Alternative:** Use percentage reduction instead of separate retentions.

Best Practices
==============

**1. Document release conditions clearly:**

.. code-block:: text

   GOOD:
   Name: Warranty Retention
   Description: Released 12 months after substantial completion,
   provided no defects reported and final inspection passed

   BAD:
   Name: Retention
   Description: Released later

**2. Use standard percentages:**

Align with industry standards and contract terms:

- Performance: 10%
- Warranty: 5%
- Tax withholding: Per jurisdiction

**3. Set up retentions before first estimate:**

Ensures consistent application across all payments.

**4. Track release dates:**

Add calendar reminders for:

- Substantial completion date + warranty period
- Milestone achievement dates
- Tax filing deadlines

**5. Reconcile regularly:**

Monthly reconciliation:

- Verify cumulative retained amounts
- Check against contract terms
- Confirm release dates are current

**6. Separate tax withholdings:**

Keep tax retentions separate from performance/warranty retentions for accounting clarity.

Common Scenarios
================

Scenario 1: Standard Construction Contract
-------------------------------------------

**Setup:**

- $1,000,000 contract
- 10% performance retention
- 5% warranty retention (released after 1 year)

**Configuration:**

.. code-block:: text

   Retention 1:
   Name: Performance Guarantee
   Percentage: 10.00%
   Release: Upon contract completion

   Retention 2:
   Name: Warranty Holdback
   Percentage: 5.00%
   Release: 1 year after substantial completion

**Estimate Flow:**

.. code-block:: text

   Estimate #1: $100,000
   Performance Retention (10%): -$10,000
   Warranty Retention (5%): -$5,000
   Net Payment: $85,000

   [... multiple estimates ...]

   At Completion:
   Total Retained: $150,000 ($100k performance + $50k warranty)

   Release Performance Retention: +$100,000
   Remaining: $50,000 (warranty held for 1 year)

   After 1 Year:
   Release Warranty Retention: +$50,000
   Balance: $0

Scenario 2: Subcontractor Agreement
------------------------------------

**Setup:**

- Simple percentage retention
- Released upon proof of payment to suppliers

**Configuration:**

.. code-block:: text

   Name: Subcontractor Retention
   Percentage: 5.00%
   Description: Released upon submission of lien waivers
   and proof of supplier payments

**Release Process:**

1. Subcontractor submits final lien waivers
2. Provides supplier payment receipts
3. Retention marked as released
4. Final payment issued

Scenario 3: Tax Withholding (Mexico Example)
---------------------------------------------

**Setup:**

- IVA (VAT) retention required by law
- 2/3 of IVA withheld and remitted to SAT

**Configuration:**

.. code-block:: text

   Name: IVA Retention
   Percentage: 10.67% (2/3 of 16% IVA)
   Description: VAT withholding per Article 1-A LIVA
   Notes: Remitted monthly to SAT

**Handling:**

- Withheld from each estimate
- Remitted to tax authority by client
- Contractor credits against tax liability
- Not "released" back to contractor

Reporting
=========

Available Reports
-----------------

**Retention Balance Report:**

Shows current retention balances by:

- Contract
- Retention type
- Client
- Status (active vs. released)

**Retention Activity Report:**

Tracks retention movements:

- Amounts withheld by period
- Release transactions
- Cumulative balances over time

**Client Retention Statement:**

For client communication:

- Total retained to date
- Breakdown by retention type
- Scheduled release dates
- Release conditions status

..
   SCREENSHOT RECOMMENDED: Retention balance report showing contract-by-contract breakdown

Export Options
--------------

- **PDF:** Formatted retention statements
- **Excel:** Detailed retention transaction history
- **CSV:** For import into accounting systems

Troubleshooting
===============

**Retention not applying to estimates:**

- Verify retention is attached to correct contract
- Check retention percentage is set (not 0%)
- Ensure retention is not already marked as "Released"
- Confirm estimate is for the correct contract

**Retention amount incorrect:**

- Review retention percentage calculation
- Check if multiple retentions are configured (additive)
- Verify estimate subtotal is correct
- Confirm no manual adjustments were made

**Can't release retention:**

- Verify you have appropriate permission level
- Check release conditions are met and documented
- Ensure retention is associated with correct contract
- Confirm retention hasn't already been released

**Multiple retention types confusing:**

- Use clear, descriptive names for each type
- Add detailed descriptions explaining release conditions
- Consider color-coding or tagging retention types
- Document in contract notes which retentions apply

Integration with Accounting
============================

Retention accounting considerations:

**Accounts Receivable:**

Retained amounts are:

- Still owed to contractor (asset)
- Recorded as "Retention Receivable"
- Recognized as revenue when earned
- Collected when released

**Client Perspective:**

Retained amounts are:

- Liability to contractor
- Recorded as "Retention Payable"
- Held until release conditions met
- Paid upon release

**Journal Entry (Contractor):**

.. code-block:: text

   When Retention Withheld:
   DR Retention Receivable  $10,000
      CR Revenue                       $10,000

   When Retention Released:
   DR Cash                  $10,000
      CR Retention Receivable          $10,000

See Also
========

- :doc:`estimates` - How retentions apply to estimates
- :doc:`projects-contracts` - Contract setup with retentions
- :doc:`/user-guide/workflows/managing-estimates` - Estimate workflows
- :doc:`/_glossary/domain-terms` - Complete terminology
