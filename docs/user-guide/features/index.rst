========
Features
========

Discover Construbot's powerful capabilities for construction management.

Key Features
============

Hierarchical Contracts
----------------------

**Parent-child contract relationships** for complex project structures:

- Link subcontracts to main contracts
- Track costs across multiple levels
- Rollup reporting for project totals
- Independent estimates for each level

**Use cases:**
- General contractor with multiple subcontractors
- Phased projects with separate billing
- Multi-building developments

See :doc:`/user-guide/concepts/projects-contracts` for details.

Progress Billing & Estimates
-----------------------------

**Automated estimate generation** with cumulative tracking:

- Create progress estimates (estimaciones) easily
- Automatic cumulative quantity calculation
- Retention tracking and management
- Over-billing prevention warnings
- Professional PDF generation

**Financial accuracy:**
- Real-time subtotal calculation
- Multiple retention types supported
- Advance payment amortization
- Payment history tracking

See :doc:`/user-guide/concepts/estimates` for details.

Excel Integration
-----------------

**Bulk import capabilities** for efficient data entry:

- **Concept Catalogs**: Import hundreds of line items at once
- **Retentions**: Upload retention structures from templates
- **Data Export**: Generate Excel reports for analysis

**Benefits:**
- Save hours on manual data entry
- Reduce errors with validated imports
- Use existing estimating tools
- Standardize across projects

See :doc:`/user-guide/concepts/concepts-line-items` for catalog management.

Multi-Company Support
---------------------

**Single installation, multiple companies:**

- Complete data isolation between companies
- User access to multiple companies
- Switch active company seamlessly
- Company-specific configurations

**Perfect for:**
- Holding companies with subsidiaries
- Partnerships managing separate entities
- Contractors with multiple business licenses

Document Generation
-------------------

**Professional PDF documents** for all project needs:

- **Estimates**: Detailed progress billing documents
- **Contracts**: Complete contract documentation
- **Reports**: Financial and progress reports
- **Custom Templates**: Branded documents with logo

**Features:**
- Automatic formatting
- Multiple recipients support
- Email delivery integration
- Archive and tracking

Retention Management
--------------------

**Comprehensive retention tracking:**

- **Multiple retention types**: Performance, warranty, tax withholdings
- **Automatic calculation**: Applied to each estimate
- **Release tracking**: Monitor retention balances
- **Partial releases**: Progressive release support

**Financial control:**
- Cumulative retention balance tracking
- Release date reminders
- Accounting integration ready

See :doc:`/user-guide/concepts/retentions` for details.

Site & Contact Management
-------------------------

**Organize project locations and communications:**

- **Multiple sites per client**: Separate locations easily
- **Contact management**: Track recipients for documents
- **GPS coordinates**: Remote site support
- **Communication history**: Track approvals and submissions

See :doc:`/user-guide/concepts/sites-contacts` for details.

Security & Permissions
----------------------

**Role-based access control:**

- **Six permission levels**: From Auxiliar to Superusuario
- **Granular permissions**: Control who can create, edit, approve
- **Audit trails**: Track all changes and actions
- **Data isolation**: Company-level security

**Permission levels:**
- Auxiliar (Assistant)
- Coordinador (Coordinator)
- Director
- Corporativo (Corporate)
- Soporte (Support)
- Superusuario (Super User)

Advanced Features
=================

Tree-Based Contract Hierarchy
------------------------------

Powered by **django-treebeard** for efficient hierarchical data:

- Materialized Path implementation
- Fast tree queries and navigation
- Unlimited nesting levels
- Ancestor/descendant calculations

API Access
----------

**REST API** with JWT authentication:

- Full CRUD operations on all entities
- Secure token-based authentication
- JSON data interchange
- Integration with external systems

See :doc:`/developer/api/index` for API documentation.

Customization
-------------

**Flexible configuration options:**

- Custom retention types and percentages
- Configurable document templates
- Company-specific settings
- Field validation rules

Future Features
===============

Planned enhancements:

- Mobile application (iOS/Android)
- Advanced analytics dashboard
- Accounting software integrations
- Multi-currency support
- Equipment tracking
- Time & labor management

Need More Information?
======================

- :doc:`/user-guide/concepts/index` - Understand core concepts
- :doc:`/user-guide/workflows/index` - Step-by-step guides
- :doc:`/developer/index` - Technical documentation
- :doc:`/user-guide/faq` - Common questions
