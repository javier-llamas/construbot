=========
Estimates
=========

.. note::
   **Spanish Term:** Estimación

Understanding estimates (progress payments) in Construbot.

What is an Estimate?
====================

An **Estimate** (Spanish: **Estimación**) is a progress payment request for completed work on a construction project. Estimates document:

- Work completed during a specific period
- Quantities of each concept (line item) executed
- Payment amount owed for the period
- Cumulative progress tracking

**Model:** ``construbot.proyectos.models.Estimate``

**Key Concept:** Estimates are tied to contracts and track incremental billing as work progresses. Each estimate builds upon previous estimates to show cumulative project completion.

..
   SCREENSHOT RECOMMENDED: Estimate list view showing multiple estimates for a contract

Estimate Components
===================

Basic Information
-----------------

**Required fields:**

- **Contract** (contrato) - The parent contract being billed
- **Estimate Number** (consecutive number) - Sequential identifier
- **Period Start Date** (fecha_inicio_estimado)
- **Period End Date** (fecha_final_estimado)
- **Total Amount** (monto) - Calculated from line items

**Optional fields:**

- **Notes** (notas) - Internal notes about the estimate
- **Status** - Draft, submitted, approved, paid
- **Approval Date**
- **Payment Date**

..
   SCREENSHOT RECOMMENDED: Estimate creation form showing all fields

Line Items (EstimateLineItems)
-------------------------------

Each estimate contains multiple line items tracking individual concept progress:

- **Concept** (concepto) - Reference to catalog concept
- **Quantity This Period** (cantidad_estimada) - Work completed this period
- **Cumulative Quantity** (cantidad_acumulada) - Total work to date
- **Unit Price** (precio_unitario) - From contract concept
- **Subtotal** (subtotal) - Quantity × Unit Price

**Related Model:** ``construbot.proyectos.models.EstimateLineItem``

..
   SCREENSHOT RECOMMENDED: Estimate detail view showing line items table with quantities and amounts

Financial Calculations
======================

Estimate Amount Calculation
----------------------------

The estimate total is calculated as:

.. code-block:: text

   Subtotal = Sum of (Quantity This Period × Unit Price) for all line items

   Retentions = Subtotal × Retention Percentage(s)

   Estimate Total = Subtotal - Retentions

   Amount to Pay = Estimate Total - Previous Balance (if applicable)

**Example:**

.. code-block:: text

   Line Items:
   - Excavation: 150 m³ × $200/m³ = $30,000
   - Concrete: 80 m³ × $1,500/m³ = $120,000
   - Rebar: 2,500 kg × $15/kg = $37,500

   Subtotal: $187,500
   Retention (10%): -$18,750
   Estimate Total: $168,750

Cumulative Tracking
-------------------

Construbot automatically tracks cumulative quantities:

1. **Previous Estimates:** Sum of all prior estimate quantities
2. **This Estimate:** New work completed
3. **Cumulative Total:** Running total of all work to date
4. **Remaining:** Contract quantity - Cumulative total

This ensures you never over-bill a contract concept.

..
   SCREENSHOT RECOMMENDED: Estimate line item showing previous, current, and cumulative quantities

Retentions (Withholdings)
--------------------------

Retentions can be applied to estimates:

- **Flat percentage:** 10% retention on all work
- **Multiple retentions:** Different percentages for different purposes (warranty, performance)
- **Retention release:** Held until contract completion or milestones

See :doc:`retentions` for detailed information.

Creating an Estimate
=====================

Step 1: Access Contract
------------------------

1. Navigate to **Proyectos → Contratos**
2. Select the contract you want to bill
3. Click **"Create Estimate"** or **"Nueva Estimación"**

..
   SCREENSHOT RECOMMENDED: Contract detail page with "Create Estimate" button highlighted

Step 2: Set Estimate Period
----------------------------

.. code-block:: text

   Period Start: 2024-01-01
   Period End: 2024-01-31
   Estimate Number: Auto-assigned (e.g., Estimate #3)

Step 3: Add Line Items
-----------------------

For each concept with work completed:

1. Select the concept from contract catalog
2. Enter **Quantity This Period** (work completed)
3. System calculates:
   - Cumulative quantity
   - Subtotal (quantity × unit price)
   - Warnings if exceeding contract quantity

**Example Entry:**

.. code-block:: text

   Concept: Excavation (Contract Qty: 500 m³)
   Previous Estimates: 200 m³
   This Estimate: 150 m³
   Cumulative: 350 m³
   Remaining: 150 m³

   Unit Price: $200/m³
   Subtotal: $30,000

Step 4: Review Totals
----------------------

Before saving, review:

- **Subtotal:** Sum of all line items
- **Retentions:** Applied percentages
- **Estimate Total:** Amount to be paid
- **Cumulative Progress:** Overall project completion

..
   SCREENSHOT RECOMMENDED: Estimate summary section showing subtotal, retentions, and total

Step 5: Save and Generate Documents
------------------------------------

1. Click **"Save"** or **"Guardar"**
2. Generate PDF estimate document
3. Submit for approval (if workflow configured)
4. Track payment status

Estimate Workflow
=================

Typical Process
---------------

1. **Draft:** Initial creation, can be edited
2. **Submitted:** Sent to client for review
3. **Under Review:** Client reviewing estimate
4. **Approved:** Client approved, ready for payment
5. **Paid:** Payment received and recorded

**Workflow Configuration:** May vary by company and contract type.

..
   SCREENSHOT RECOMMENDED: Estimate status workflow diagram or status field dropdown

Revisions and Corrections
--------------------------

If an estimate needs correction:

**Option 1: Edit Draft**

- If status is still "Draft", edit directly
- Update line item quantities as needed

**Option 2: Create Adjustment**

- If estimate is approved, create a new estimate
- Use negative quantities to reverse errors
- Add corrected quantities in same or next estimate

**Best Practice:** Add notes explaining any adjustments for audit trail.

Hierarchical Contracts
======================

For subcontracts using hierarchical structure:

**Parent Contract Estimate:**

- Parent estimate includes own work + subcontract estimates
- Subcontract estimates roll up automatically
- System prevents double-counting

**Subcontract Estimate:**

- Created independently for subcontractor work
- Linked to parent contract estimate
- Separate billing and payment tracking

See :doc:`projects-contracts` for hierarchy details.

Best Practices
==============

**1. Regular billing cycles:**

.. code-block:: text

   GOOD: Weekly or monthly estimates with consistent periods
   BAD: Irregular estimates with gaps or overlaps

**2. Document justification:**

Add notes explaining:
- Unusual quantities
- Zero-quantity periods (weather delays, etc.)
- Adjustments or corrections

**3. Review cumulative totals:**

Before submitting, verify:
- No concepts exceed contract quantity
- Cumulative percentages make sense
- Previous estimates are correctly summed

**4. Coordinate with site progress:**

- Estimates should reflect actual completed work
- Use site photos or daily reports as backup
- Don't estimate work not yet performed

**5. Track payment timing:**

- Record when estimate submitted
- Follow up on approvals
- Document payment receipt

Reporting and Analysis
======================

Estimate Reports
----------------

Available reports:

- **Estimate Summary:** Single estimate with all line items
- **Contract Progress:** All estimates for a contract showing cumulative progress
- **Payment Schedule:** Estimate amounts vs. payment dates
- **Retention Tracking:** Retained amounts and releases

**Export Options:** PDF, Excel

..
   SCREENSHOT RECOMMENDED: Estimate report or PDF document preview

Financial Metrics
-----------------

Track project health:

- **Billing Rate:** Actual billed vs. planned
- **Payment Lag:** Time from estimate submission to payment
- **Retention Balance:** Total retained amounts
- **Completion Percentage:** Cumulative quantities vs. contract quantities

Common Scenarios
================

Scenario 1: First Estimate
---------------------------

**Setup:**

- New contract with 10 concepts
- Work started, first month completed
- 3 concepts have progress

**Process:**

1. Create Estimate #1 for Month 1
2. Add 3 line items with quantities
3. Review subtotal and retentions
4. Generate PDF and submit

**Result:** Establishes baseline for cumulative tracking.

Scenario 2: Zero-Work Period
-----------------------------

**Situation:** Weather delay, no work completed in period

**Options:**

1. **Skip estimate:** Don't create estimate for period (creates gap in numbering)
2. **Zero estimate:** Create estimate with explanation in notes

**Recommendation:** Create zero estimate with notes explaining delay for complete audit trail.

Scenario 3: Over-Billing Prevention
------------------------------------

**Situation:** Trying to bill 200 m³ but only 150 m³ remain on contract

**System Behavior:**

- Warning displayed when quantity exceeds remaining
- Can still save if justified (change orders, variations)
- Flags for review

**Resolution:**

- Adjust quantity to 150 m³, or
- Create change order to increase contract quantity first

Troubleshooting
===============

**Can't create estimate:**

- Verify contract has concepts in catalog
- Check contract status is active
- Confirm user has permission level (Coordinador or higher)

**Quantities not calculating:**

- Ensure unit prices are set on contract concepts
- Verify previous estimates are saved and approved
- Check for database sync issues (rare)

**Retentions incorrect:**

- Review retention configuration on contract
- Verify retention percentages are current
- Check if retentions should apply to this estimate type

**PDF generation fails:**

- Verify template files exist
- Check media storage permissions
- Review error logs for specific issue

See Also
========

- :doc:`projects-contracts` - Parent contracts
- :doc:`concepts-line-items` - Understanding concepts
- :doc:`retentions` - Withholdings and releases
- :doc:`/user-guide/workflows/managing-estimates` - Estimate workflow guide
- :doc:`/_glossary/domain-terms` - Complete terminology
