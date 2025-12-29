=====================
Translation Glossary
=====================

Spanish→English translation reference for contributors.

Overview
========

The Construbot codebase uses Spanish terminology for business entities. This glossary provides canonical English translations for consistency.

Master Glossary
================

.. note::
   **Complete Glossary:** See :doc:`/_glossary/domain-terms` for the comprehensive 100+ term glossary with descriptions, model references, and examples.

Quick Reference
===============

Core Business Terms
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Spanish
     - English
     - Model
   * - Contrato
     - Contract / Project
     - proyectos.models.Contrato
   * - Contraparte
     - Counterparty
     - proyectos.models.Contraparte
   * - Estimación
     - Estimate / Progress Payment
     - proyectos.models.Estimate
   * - Concepto
     - Concept / Line Item
     - proyectos.models.Concept
   * - Retención
     - Retention / Withholding
     - proyectos.models.Retenciones
   * - Sitio
     - Site
     - proyectos.models.Sitio
   * - Destinatario
     - Recipient / Contact
     - proyectos.models.Destinatario

Counterparty Types
------------------

.. list-table::
   :header-rows: 1

   * - Spanish
     - English
   * - Cliente
     - Client
   * - Destajista
     - Piecework Contractor
   * - Subcontratista
     - Subcontractor

Field Names
-----------

.. list-table::
   :header-rows: 1

   * - Spanish
     - English
   * - folio
     - reference_number
   * - monto
     - amount
   * - anticipo
     - advance_payment
   * - fecha_inicio
     - start_date
   * - fecha_fin
     - end_date

Translation Guidelines
======================

**1. Use canonical translations:**

Follow the master glossary for consistency.

**2. Context matters:**

- **Contrato** = "Contract" (legal), "Project" (colloquial)
- **Estimación** = "Estimate" (technical), "Progress Payment" (financial)

**3. Preserve Spanish in code:**

Don't rename model fields - keep Spanish names, translate in documentation.

**4. First use pattern:**

.. code-block:: rst

   Contracts (Spanish: Contratos) are the main business entity...

**5. Model references:**

Always reference the model when introducing terms:

.. code-block:: rst

   **Contraparte** (``proyectos.models.Contraparte``) represents...

Contributing Translations
==========================

**Add new terms:**

1. Add to :doc:`/_glossary/domain-terms`
2. Include: Spanish term, English translation, description, model reference, examples
3. Alphabetize within category
4. Submit pull request

**Update existing terms:**

1. Discuss in GitHub issue first
2. Update master glossary
3. Update all affected documentation
4. Submit pull request

Django Translation
==================

**For UI strings:**

.. code-block:: bash

   # Extract messages
   python manage.py makemessages -l es

   # Edit .po files
   # locale/es/LC_MESSAGES/django.po

   # Compile
   python manage.py compilemessages

See Also
========

- :doc:`/_glossary/domain-terms` - Complete 100+ term glossary
- :doc:`../getting-started` - Contributor setup
- :doc:`/developer/architecture/multi-tenancy` - Architecture context
