===
FAQ
===

Frequently asked questions about using Construbot.

General Questions
=================

What is Construbot?
-------------------

Construbot is an operational management solution for construction companies. It helps manage contracts, track progress payments (estimates), handle financial calculations, and generate professional documents.

See :doc:`introduction` for a complete overview.

Who should use Construbot?
---------------------------

Construbot is designed for:

- **Project Managers** - Track project progress and billing
- **Contract Administrators** - Manage contracts and documents
- **Accounting Staff** - Handle financial tracking and payments
- **Site Supervisors** - Report completed work
- **Directors** - Overview of all projects and finances

What does "Construbot" mean?
-----------------------------

"Construbot" is a combination of "Construction" + "Robot" - an automated solution for construction operations.

Getting Started
===============

How do I log in for the first time?
------------------------------------

1. Navigate to your Construbot URL
2. Enter your email and password (provided by administrator)
3. Click "Login"
4. You'll be directed to the dashboard

If you don't have credentials, contact your system administrator.

How do I change my password?
-----------------------------

1. Click your username in the top-right
2. Select "Profile" or "Change Password"
3. Enter current password
4. Enter new password twice
5. Click "Save"

Which company am I working in?
-------------------------------

Your **active company** is shown in the top navigation bar. If you have access to multiple companies:

1. Click the company name dropdown
2. Select the company you want to work in
3. All data will switch to that company

Contracts & Projects
====================

What's the difference between a contract and a project?
--------------------------------------------------------

In Construbot, **"Contract" (Contrato)** and **"Project"** are the same thing. The term "Contract" is used because it represents the legal agreement, but it functions as a project management entity.

How do I create a new contract?
--------------------------------

See the complete workflow in :doc:`workflows/index` (Creating a New Project section).

**Quick steps:**
1. Create client counterparty
2. Create site
3. Create contract
4. Add concept catalog
5. Add contacts

Can I have subcontracts under a main contract?
-----------------------------------------------

Yes! Construbot supports **hierarchical contracts**. When creating a subcontract, select the parent contract in the contract form.

See :doc:`concepts/projects-contracts` (Hierarchical Contracts section).

Why can't I delete a contract?
-------------------------------

Contracts with associated estimates cannot be deleted to preserve financial records. Instead:

- Mark the contract as inactive
- Add a note explaining why it was closed
- It will be hidden from active contract lists

Estimates & Billing
===================

What is an "Estimate" (Estimación)?
------------------------------------

An **estimate** is a progress payment request for work completed during a specific period. It's similar to an invoice but specifically for construction progress billing.

See :doc:`concepts/estimates` for detailed information.

How do cumulative quantities work?
-----------------------------------

Construbot automatically tracks:

- **Previous estimates**: Total from all prior estimates
- **This estimate**: New work completed
- **Cumulative total**: Running total to date
- **Remaining**: Contract quantity - Cumulative

This ensures you never over-bill a contract concept.

What are retentions?
--------------------

**Retentions** are percentages withheld from payments:

- **Performance retention** (5-10%): Held until completion
- **Warranty retention** (5%): Held during warranty period
- **Tax withholdings**: Government-required deductions

See :doc:`concepts/retentions` for details.

How do I fix an incorrect estimate?
------------------------------------

**If still in draft:**
- Edit the estimate directly
- Update quantities as needed

**If already approved:**
- Create a new estimate
- Use negative quantities to reverse errors
- Add corrected quantities
- Document in notes

Can I delete an estimate?
--------------------------

Estimates associated with payments cannot be deleted. Instead:

- Create a correcting estimate (negative quantities)
- Or mark as void and create a new one
- Add notes explaining the correction

Counterparties & Sites
=======================

What is a "Counterparty" (Contraparte)?
----------------------------------------

A **counterparty** is any business entity you work with:

- **Cliente** (Client): Companies that hire you
- **Subcontratista** (Subcontractor): Specialized contractors you hire
- **Destajista** (Piecework Contractor): Paid by completed units

See :doc:`concepts/counterparties` for details.

Can I have multiple sites for one client?
------------------------------------------

Yes! Create as many sites as needed for each client. Each contract is then associated with a specific site.

**Example**: National retail chain with stores in multiple cities - create one client and multiple sites.

What are "Contacts" (Destinatarios)?
-------------------------------------

**Contacts** are individuals who receive documents for a specific contract:

- Project managers
- Accounts payable staff
- Site supervisors

They're contract-specific, so the same person can be a contact on multiple contracts.

See :doc:`concepts/sites-contacts` for details.

Data Import/Export
==================

Can I import my existing project catalogs?
------------------------------------------

Yes! Import concept catalogs from Excel:

1. Prepare Excel with: Code, Description, Unit, Quantity, Unit Price
2. In contract view, click "Import from Excel"
3. Map columns
4. Verify and import

See :doc:`concepts/concepts-line-items` (Method 2: Excel Import).

Can I export data to Excel?
----------------------------

Yes! Most views have an "Export" button that generates Excel spreadsheets:

- Contract lists
- Estimate data
- Financial reports
- Concept catalogs

What format should my Excel file be?
-------------------------------------

- **File type**: .xlsx or .xls
- **Required columns**: Depend on what you're importing (concepts, retentions, etc.)
- **No merged cells**: Keep it simple
- **Header row**: First row should have column names

Troubleshooting
===============

I can't see my contract in the list
------------------------------------

Check:

- **Active company**: Are you in the correct company?
- **Filters**: Any active filters limiting the list?
- **Permissions**: Do you have access to view this contract?
- **Status**: Is the contract marked as inactive?

Calculations seem wrong
-----------------------

Verify:

- **Unit prices**: Check concept unit prices are correct
- **Quantities**: Ensure quantities are in correct units
- **Retentions**: Verify retention percentages
- **Previous estimates**: Check cumulative totals

If still incorrect, check for:
- Decimal place errors
- Manual overrides
- Data entry mistakes

I can't generate a PDF
-----------------------

Common causes:

- **No line items**: Estimate must have at least one line item
- **Missing data**: Check all required fields are filled
- **Permissions**: Verify you have permission to generate PDFs
- **Template issues**: Contact administrator if template is missing

Error messages in Spanish
--------------------------

The application interface uses Spanish terminology, but error messages should be clear. Common terms:

- **"Contrato"** = Contract
- **"Estimación"** = Estimate
- **"Concepto"** = Concept/Line Item
- **"Retención"** = Retention

See :doc:`/reference/glossary` for complete Spanish-English translations.

Permissions & Access
====================

What are the permission levels?
--------------------------------

Six levels from lowest to highest:

1. **Auxiliar** (Assistant): Basic read access
2. **Coordinador** (Coordinator): Create and edit projects
3. **Director**: Approve estimates, full project access
4. **Corporativo** (Corporate): Multi-company access
5. **Soporte** (Support): System support functions
6. **Superusuario** (Super User): Full system access

I don't have permission to do something
----------------------------------------

Contact your system administrator or company director to:

- Request higher permission level
- Get access to specific companies
- Request specific feature access

Technical Issues
================

The page won't load
-------------------

Try:

1. Refresh the page (F5 or Ctrl+R)
2. Clear browser cache
3. Try a different browser
4. Check internet connection
5. Contact IT support if problem persists

Data isn't saving
-----------------

Check:

- **Required fields**: All required fields filled?
- **Validation errors**: Any error messages shown?
- **Permissions**: Do you have save permission?
- **Browser console**: Press F12 and check for JavaScript errors

Getting Help
============

Where can I find more documentation?
-------------------------------------

- **User Guide**: :doc:`index` (this section)
- **Developer Docs**: :doc:`/developer/index`
- **Contributor Guide**: :doc:`/contributor/index`
- **Glossary**: :doc:`/reference/glossary`

How do I report a bug?
----------------------

See :doc:`/contributor/issue-reporting` for bug reporting guidelines.

Include:
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if relevant
- Your permission level and company

How do I request a feature?
----------------------------

Open an issue on GitHub with:

- Clear description of the feature
- Use case / business need
- How it would benefit users

Who do I contact for support?
------------------------------

- **Technical issues**: Your IT administrator
- **Account/Access**: Your company director
- **Bug reports**: GitHub issues
- **Feature requests**: GitHub discussions

Still Have Questions?
=====================

- Check other documentation sections: :doc:`concepts/index`, :doc:`workflows/index`, :doc:`features/index`
- Review the :doc:`/reference/glossary` for terminology
- Contact your system administrator
- Open a discussion on GitHub

.. tip::
   **Can't find your answer?** The search function (top-right) searches all documentation.
   Try searching for key terms in English or Spanish.
