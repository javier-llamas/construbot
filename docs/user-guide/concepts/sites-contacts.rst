================
Sites & Contacts
================

.. note::
   **Spanish Terms:** Sitio, Destinatario

Understanding sites (construction locations) and contacts (recipients) in Construbot.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

Construbot uses two related concepts for location and communication:

- **Sites** (Spanish: **Sitios**) - Physical locations where work is performed
- **Contacts** (Spanish: **Destinatarios**) - Individuals who receive documents and communications

Together, these enable proper project location tracking and document routing.

Sites (Sitios)
==============

What is a Site?
---------------

A **Site** (Spanish: **Sitio**) is a physical construction location associated with a client. Sites represent:

- Specific job sites or work locations
- Buildings or facilities under construction
- Physical addresses where work occurs
- Locations for contract execution

**Model:** ``construbot.proyectos.models.Sitio``

**Key Relationships:**

- Each site belongs to exactly one **Client** counterparty
- Multiple sites can belong to the same client
- Contracts are associated with specific sites
- Sites enable location-based project organization

..
   SCREENSHOT RECOMMENDED: Site list view showing multiple sites for different clients

Site Information
----------------

**Required fields:**

- **Name** (nombre) - Descriptive name of the site
- **Client** (cliente) - The client counterparty who owns this site
- **Company** - Your company (for multi-tenant isolation)

**Optional fields:**

- **Address** (dirección) - Full street address
- **City** (ciudad)
- **State** (estado)
- **Postal Code** (código postal)
- **Country** (país)
- **GPS Coordinates** (latitud, longitud)
- **Contact Phone** (teléfono)
- **Site Manager** - Person responsible for the site
- **Notes** (notas) - Additional information

..
   SCREENSHOT RECOMMENDED: Site detail form showing all address fields

Creating a Site
---------------

Step 1: Navigate to Sites
^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Log in to Construbot
2. Navigate to **Proyectos → Sitios**
3. Click **"New Site"** or **"Agregar Sitio"**

Step 2: Select Client
^^^^^^^^^^^^^^^^^^^^^^

Choose the client who owns this site from the dropdown.

**Note:** Only **Client** type counterparties appear in this list.

Step 3: Enter Site Details
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Name: Office Building - Downtown Plaza
   Client: Acme Construction Inc.

   Address: 123 Main Street
   City: Mexico City
   State: CDMX
   Postal Code: 06000

   GPS: 19.4326, -99.1332 (optional)
   Phone: +52 55 1234 5678
   Site Manager: John Smith

Step 4: Save
^^^^^^^^^^^^^

Click **"Save"** or **"Guardar"** to create the site.

..
   SCREENSHOT RECOMMENDED: New site creation form with sample data filled in

Using Sites
-----------

**In Contracts:**

When creating a contract for a client, select the specific site:

1. Choose the client counterparty
2. Site dropdown automatically filters to show only that client's sites
3. Select the appropriate site for this contract

**Multiple Contracts per Site:**

The same site can have multiple contracts:

- Different phases of work
- Separate buildings on same property
- Different trade contracts for same location

**Site-Based Reporting:**

Generate reports by site to see:

- All contracts for a location
- Total project value at site
- Active work at site
- Payment history for location

Common Site Scenarios
---------------------

**Scenario 1: Single Site Client**

- Client has one office building
- Create one site: "Main Office Building"
- All contracts for this client use this site

**Scenario 2: Multi-Location Client**

- National retail chain client
- Create separate sites:
  - "Store #101 - Dallas TX"
  - "Store #102 - Houston TX"
  - "Store #103 - Austin TX"
- Each contract specifies which store

**Scenario 3: Campus or Complex**

- University campus with multiple buildings
- Options:
  - **One site:** "University Campus" (simple)
  - **Multiple sites:** "Science Building", "Library", "Dorms" (detailed)

Choose based on reporting and organization needs.

Contacts (Destinatarios)
========================

What is a Contact?
------------------

A **Contact** (Spanish: **Destinatario**, literally "recipient") is an individual who receives documents or communications related to a contract. Contacts represent:

- People who receive estimates, invoices, reports
- Project managers or supervisors
- Client representatives
- Document approvers

**Model:** ``construbot.proyectos.models.Destinatario``

**Key Concept:** Contacts are specific to a contract, not global. The same person may be a contact on multiple contracts.

..
   SCREENSHOT RECOMMENDED: Contact list within a contract showing multiple recipients

Contact Information
-------------------

**Required fields:**

- **Name** (nombre) - Full name of the person
- **Contract** (contrato) - Which contract they're associated with

**Optional fields:**

- **Position** (puesto) - Job title or role
- **Email** (correo) - Email address
- **Phone** (teléfono) - Contact phone number
- **Department** (departamento) - Organizational unit
- **Notes** (notas) - Additional information
- **Active** (activo) - Whether they should receive documents

**Document Delivery:**

When generating PDFs or sending emails, the system can automatically include all active contacts for a contract.

..
   SCREENSHOT RECOMMENDED: Contact form showing all fields including position, email, phone

Creating a Contact
------------------

Step 1: Access Contract
^^^^^^^^^^^^^^^^^^^^^^^

Contacts are created within a specific contract:

1. Navigate to the contract
2. Find the **"Contacts"** or **"Destinatarios"** section
3. Click **"Add Contact"** or **"Agregar Destinatario"**

Step 2: Enter Contact Details
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Name: María González
   Position: Project Manager
   Email: maria.gonzalez@client.com
   Phone: +52 55 9876 5432
   Department: Construction Division
   Active: Yes

Step 3: Save
^^^^^^^^^^^^^

Click **"Save"** to add this contact to the contract.

**Repeat** for additional contacts on the same contract.

Using Contacts
--------------

**Document Generation:**

When generating estimate PDFs or reports:

1. System includes "To:" field with all active contacts
2. Email delivery can CC all contact email addresses
3. Each contact receives relevant project documents

**Communication Tracking:**

Contacts help track:

- Who approved estimates
- Who received invoices
- Who to notify of project changes
- Communication history

**Multiple Contacts:**

Contracts can have multiple contacts for different purposes:

- **Primary Contact:** Main project manager
- **Financial Contact:** Accounts payable person
- **Technical Contact:** Site engineer or supervisor

Mark all as active or selectively activate based on document type.

..
   SCREENSHOT RECOMMENDED: Estimate PDF showing "To:" section with multiple contacts listed

Best Practices
==============

Sites
-----

**1. Use descriptive names:**

.. code-block:: text

   GOOD: "Office Tower - 123 Main St, Dallas"
   BAD: "Site 1"

**2. Include location identifiers:**

For chains or franchises:

.. code-block:: text

   GOOD: "McDonald's #4521 - Austin Airport"
   BAD: "McDonald's Austin"

**3. Keep addresses current:**

Update addresses if they change or if initial address was incomplete.

**4. Use GPS coordinates for remote sites:**

Especially useful for:

- Rural construction sites
- Sites without formal addresses
- Integration with mapping tools

**5. One site per distinct location:**

Don't create duplicate sites for the same physical location.

Contacts
--------

**1. Keep contact info current:**

Update email and phone when:

- Contact person changes roles
- New project manager assigned
- Contact information changes

**2. Use position/department fields:**

Helps identify contacts when names change:

.. code-block:: text

   Name: John Smith
   Position: Senior Project Manager
   Department: Commercial Construction

**3. Mark inactive when appropriate:**

Don't delete contacts (preserves history), mark as inactive instead:

- Person leaves company
- Contract phase changes
- Different person takes over

**4. Multiple contacts for different purposes:**

.. code-block:: text

   Contact 1: Project Manager (technical approvals)
   Contact 2: Accounts Payable (invoice delivery)
   Contact 3: Site Supervisor (daily reports)

**5. Include mobile numbers:**

For urgent communication and field contacts.

Relationship Between Sites and Contacts
========================================

**Independent but Related:**

- **Sites** are associated with **clients** (counterparties)
- **Contacts** are associated with **contracts**
- A contract links a client (and their site) with specific contacts

**Example Flow:**

.. code-block:: text

   1. Client: "National Retail Corp"
   2. Site: "Store #101 - Dallas TX"
   3. Contract: "C-2024-001" for Store #101
   4. Contacts:
      - Sarah Johnson (Store Manager)
      - Mike Chen (Regional Supervisor)

When you generate an estimate for contract C-2024-001:

- **Site information** appears on document header (location)
- **Contact information** appears in "To:" field (recipients)

..
   SCREENSHOT RECOMMENDED: Contract detail page showing site selection and contacts section together

Reporting
=========

Site-Based Reports
------------------

Generate reports filtered by site:

- **Contracts by Site:** All contracts for a location
- **Financial Summary by Site:** Total revenue per site
- **Active Projects by Site:** Current work at each location
- **Site Portfolio:** All sites for a client with contract counts

Contact Reports
---------------

- **Contact List:** All contacts across contracts
- **Document Distribution:** Who received which documents
- **Active Contacts:** Currently active recipients
- **Contact History:** Communication tracking over time

Troubleshooting
===============

Sites
-----

**Can't find site when creating contract:**

- Verify site is associated with correct client counterparty
- Check that site belongs to your active company
- Ensure client is marked as active

**Duplicate sites appearing:**

- Review site names and addresses
- Consolidate duplicates by:
  1. Updating contracts to use correct site
  2. Marking duplicate site as inactive
  3. Adding notes explaining consolidation

**Site address changes:**

- Update site address directly
- Existing contracts automatically reference new address
- Consider adding note about address change date

Contacts
--------

**Contact not receiving documents:**

- Verify contact is marked as "Active"
- Check email address is correct
- Confirm contact is associated with correct contract
- Review email delivery logs

**Wrong contact on documents:**

- Mark incorrect contact as inactive
- Add correct contact with accurate information
- Update any pending documents

**Contact information outdated:**

- Update contact record directly
- Changes apply to future documents only
- Past documents retain historical contact info (as intended)

See Also
========

- :doc:`counterparties` - Client counterparties who own sites
- :doc:`projects-contracts` - Contracts using sites and contacts
- :doc:`/user-guide/workflows/creating-project` - Complete project setup workflow
- :doc:`/_glossary/domain-terms` - Complete terminology
