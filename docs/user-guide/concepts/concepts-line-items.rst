====================
Concepts & Line Items
====================

.. note::
   **Spanish Term:** Concepto

Understanding concepts (individual work items) in Construbot contract catalogs.

.. contents:: Table of Contents
   :local:
   :depth: 2

What is a Concept?
==================

A **Concept** (Spanish: **Concepto**) is an individual work item in a construction contract catalog. Concepts represent:

- Specific types of work to be performed
- Measurable units of construction activities
- Line items for billing and tracking
- Building blocks of estimates

**Model:** ``construbot.proyectos.models.Concept``

**Key Relationship:** Concepts belong to a contract and define what work will be done, at what quantity, and at what price.

..
   SCREENSHOT RECOMMENDED: Concept catalog view showing multiple concepts for a contract

Concept Structure
=================

Basic Information
-----------------

**Required fields:**

- **Code** (clave) - Unique identifier within contract catalog
- **Description** (concepto) - Description of the work
- **Unit** (unidad) - Unit of measurement
- **Quantity** (cantidad) - Total contract quantity
- **Unit Price** (precio_unitario) - Price per unit
- **Contract** (contrato) - Parent contract

**Optional fields:**

- **Notes** (notas) - Additional specifications
- **Category** (categoría) - Grouping for organization
- **Order** (orden) - Display sequence
- **Active** (activo) - Whether concept is currently used

**Calculated fields:**

- **Total** (importe) - Quantity × Unit Price

..
   SCREENSHOT RECOMMENDED: Concept detail form showing all fields with sample data

Example Concept
---------------

.. code-block:: text

   Code: 001-EXC-01
   Description: Excavation for foundations, including hauling
   Unit: m³ (cubic meter)
   Quantity: 500.00
   Unit Price: $200.00
   Total: $100,000.00

   Category: Earthwork
   Notes: Depth 0-3 meters, hard soil conditions

Units of Measurement
====================

Common Units
------------

Construbot supports various measurement units:

**Linear measures:**

- **m** - Meter
- **km** - Kilometer
- **ft** - Foot

**Area measures:**

- **m²** - Square meter
- **ft²** - Square foot

**Volume measures:**

- **m³** - Cubic meter
- **L** - Liter

**Weight measures:**

- **kg** - Kilogram
- **ton** - Metric ton

**Count measures:**

- **pza** - Piece (Spanish: pieza)
- **u** - Unit
- **lot** - Lot (complete set)

**Service measures:**

- **hr** - Hour
- **day** - Day
- **month** - Month

**Model:** ``construbot.proyectos.models.Units``

Custom Units
------------

Add custom units as needed:

1. Navigate to **Units** management
2. Create new unit with abbreviation and description
3. Use in concept catalog

..
   SCREENSHOT RECOMMENDED: Units list showing various measurement units

Creating Concepts
=================

Method 1: Manual Entry
----------------------

Step 1: Access Contract Catalog
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Navigate to the contract
2. Find **"Concepts"** or **"Catálogo de Conceptos"** section
3. Click **"Add Concept"** or **"Agregar Concepto"**

Step 2: Enter Concept Details
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Code: 002-CONC-01
   Description: Concrete f'c=250 kg/cm² for foundations
   Unit: m³
   Quantity: 120.00
   Unit Price: $1,500.00

   Category: Concrete Work
   Notes: Includes formwork and reinforcement steel

Step 3: Save
^^^^^^^^^^^^^

Click **"Save"** to add this concept to the catalog.

**Repeat** for all concepts in the contract.

Method 2: Excel Import
----------------------

For large contracts with many concepts:

Step 1: Prepare Excel File
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create spreadsheet with columns:

.. code-block:: text

   Code, Description, Unit, Quantity, Unit Price, Category, Notes
   001-EXC-01, Excavation for foundations, m³, 500, 200.00, Earthwork, Depth 0-3m
   002-CONC-01, Concrete f'c=250, m³, 120, 1500.00, Concrete, With formwork

Step 2: Import to Construbot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Navigate to contract concepts section
2. Click **"Import from Excel"** or **"Importar desde Excel"**
3. Select your prepared file
4. Map columns (if not auto-detected)
5. Review and confirm import

**Benefit:** Quickly populate catalog with dozens or hundreds of concepts.

..
   SCREENSHOT RECOMMENDED: Excel import interface showing column mapping and preview

Method 3: Copy from Template
-----------------------------

If you have standard catalogs:

1. Create "template" contract with common concepts
2. When creating new contract, select **"Copy catalog from..."**
3. Choose template contract
4. All concepts copied to new contract
5. Edit quantities and prices as needed

**Use case:** Repetitive project types with similar work items.

Catalog Organization
====================

Concept Codes
-------------

Use structured coding system for organization:

**Format:** ``[Category]-[Subcategory]-[Sequence]``

**Examples:**

.. code-block:: text

   001-PREP-01: Site preparation
   001-PREP-02: Demolition
   002-EARTH-01: Excavation
   002-EARTH-02: Backfill
   003-CONC-01: Foundation concrete
   003-CONC-02: Column concrete

**Benefits:**

- Easy sorting and grouping
- Quick reference
- Professional appearance on documents

Categories
----------

Group concepts into categories:

- **Preliminary Work:** Site prep, mobilization
- **Earthwork:** Excavation, compaction
- **Concrete Work:** Foundations, slabs, columns
- **Masonry:** Block walls, brick veneer
- **Finishes:** Flooring, painting, trim
- **MEP:** Mechanical, electrical, plumbing

**Purpose:** Organize large catalogs, generate category subtotals.

Display Order
-------------

Use the **Order** field to control sequence:

- Lower numbers appear first
- Group related concepts together
- Match typical construction sequence

Using Concepts in Estimates
============================

Concept Selection
-----------------

When creating an estimate:

1. Choose concepts from contract catalog
2. Enter quantity completed this period
3. System uses unit price from catalog
4. Calculate line item subtotal automatically

**Example:**

.. code-block:: text

   Estimate #3 - March 2024

   Concept: 002-CONC-01 - Concrete f'c=250
   Contract Quantity: 120 m³
   Contract Unit Price: $1,500/m³

   Previous Estimates: 80 m³
   This Estimate: 30 m³
   Cumulative: 110 m³
   Remaining: 10 m³

   Line Item Total: 30 m³ × $1,500 = $45,000

Quantity Tracking
-----------------

Construbot tracks for each concept:

- **Contract Quantity:** Original scope
- **Billed to Date:** Cumulative from all estimates
- **Remaining:** Contract - Billed
- **Over/Under:** If billed exceeds contract

**Status Indicators:**

- ✓ Complete (100% billed)
- ⚠ Over-billed (>100%)
- ◷ In Progress (<100%)
- ○ Not Started (0%)

..
   SCREENSHOT RECOMMENDED: Concept tracking report showing contract vs. billed quantities

Price Changes
=============

Unit Price Adjustments
-----------------------

If unit price needs to change:

**Option 1: Change Order**

1. Create formal change order
2. Update concept unit price
3. Document reason in notes
4. Get client approval

**Option 2: New Concept**

1. Keep original concept as-is
2. Create new concept with adjusted price
3. Use for future estimates

**Best Practice:** Document all price changes with change order references.

Quantity Adjustments
--------------------

If contract quantity changes:

**Increase Quantity:**

1. Update concept quantity
2. Document change order
3. Difference becomes additional scope

**Decrease Quantity:**

1. Update concept quantity
2. Adjust estimates if needed
3. Credit or reduce billing

Hierarchical Contracts
======================

Concept Inheritance
-------------------

For parent-child contract structures:

**Parent Contract:**

- Contains high-level concepts
- Rolled-up quantities and prices
- Summary-level tracking

**Subcontract:**

- Detailed breakdown of parent concepts
- Independent catalog
- Separate tracking

**Relationship:** Subcontract concepts can reference parent concepts for rollup reporting.

Best Practices
==============

**1. Use clear, descriptive descriptions:**

.. code-block:: text

   GOOD: "Concrete f'c=250 kg/cm² for foundations, including formwork and reinforcement"
   BAD: "Concrete"

**2. Include specifications in description:**

Key details like:

- Material grades
- Installation methods
- Included components

**3. Consistent unit usage:**

.. code-block:: text

   GOOD: All excavation in m³, all concrete in m³
   BAD: Some excavation in m³, some in loads

**4. Logical code structure:**

Use systematic coding for easy reference.

**5. One concept = one measurable item:**

.. code-block:: text

   GOOD:
   - Excavation (m³)
   - Concrete (m³)
   - Reinforcement (kg)

   BAD:
   - Excavation including concrete and rebar (lot)

**6. Price verification:**

Before importing or saving:

- Verify unit prices match contract
- Check decimal places
- Confirm total calculations

**7. Regular catalog review:**

- Remove unused concepts (mark inactive)
- Update prices for escalation
- Correct errors promptly

Common Scenarios
================

Scenario 1: Standard Building Contract
---------------------------------------

**Setup:**

- 50 concepts across 8 categories
- Mix of quantities (m³, m², kg, pza)
- Total contract value $2,000,000

**Catalog Structure:**

.. code-block:: text

   001 - Preliminary Work
      001-PREP-01: Mobilization (lot)
      001-PREP-02: Site clearing (m²)

   002 - Earthwork
      002-EARTH-01: Excavation (m³)
      002-EARTH-02: Compaction (m³)

   003 - Concrete Work
      003-CONC-01: Foundations (m³)
      003-CONC-02: Columns (m³)

   [... continued ...]

Scenario 2: Unit Price Contract
--------------------------------

**Setup:**

- Payment based on actual quantities
- Original quantities are estimates
- Final billing based on as-built

**Process:**

1. Set up catalog with estimated quantities
2. Bill actual quantities in estimates
3. Final total may exceed or underbid original estimate
4. Document variations with notes

Scenario 3: Lump Sum Items
---------------------------

**Setup:**

- Some work paid as lump sum, not unit price

**Configuration:**

.. code-block:: text

   Code: 001-MOBILIZATION
   Description: Mobilization and general conditions
   Unit: lot
   Quantity: 1.00
   Unit Price: $50,000.00
   Total: $50,000.00

**Billing:** Bill 100% in first estimate or progressive percentage.

Reporting
=========

Catalog Reports
---------------

Available reports:

- **Complete Catalog:** All concepts with quantities and prices
- **Category Summary:** Totals by category
- **Price List:** Unit prices for reference
- **Quantity Tracking:** Contract vs. billed quantities

..
   SCREENSHOT RECOMMENDED: Concept catalog report showing all line items with totals

Progress Reports
----------------

Track project completion:

- **Percentage Complete:** By quantity for each concept
- **Value Complete:** Dollar value billed to date
- **Remaining Work:** Unbilled quantities and values

Export Options
--------------

- **PDF:** Formatted catalog for printing/sharing
- **Excel:** Editable spreadsheet for analysis
- **CSV:** For import to estimating software

Troubleshooting
===============

**Concept not appearing in estimate:**

- Verify concept is marked "Active"
- Check concept belongs to correct contract
- Confirm concept has quantity > 0
- Ensure user has permission to view

**Unit price won't update:**

- Check if concept is linked to approved estimates
- Review permission level (may require higher access)
- Confirm change order approval if required

**Total calculation incorrect:**

- Verify quantity and unit price values
- Check for decimal place errors
- Confirm proper unit of measurement
- Review for manual overrides

**Import failed:**

- Check Excel file format (must be .xlsx or .xls)
- Verify column headers match expected names
- Ensure no empty required fields
- Review for special characters in text

**Over-billing warnings:**

- Review estimate quantities vs. contract quantities
- Check if change orders increased contract scope
- Verify cumulative calculations are correct
- Document justification if intentional

Integration with Estimating
============================

If you use external estimating software:

**Export from Estimating Tool:**

1. Generate final estimate with quantities and prices
2. Export to Excel format
3. Import to Construbot as contract catalog

**Sync Pricing:**

- Keep Construbot catalog as master
- Export for estimating template
- Import updated pricing after bid

See Also
========

- :doc:`projects-contracts` - Contract setup and structure
- :doc:`estimates` - Using concepts in estimates
- :doc:`/user-guide/workflows/importing-catalogs` - Excel import workflows
- :doc:`/_glossary/domain-terms` - Complete terminology
