========
Glossary
========

Quick reference for Spanish→English terminology.

.. note::
   **Complete Glossary:** See :doc:`/_glossary/domain-terms` for the comprehensive glossary with 100+ terms, descriptions, and examples.

Common Terms
============

.. glossary::

   Contrato
      Contract or Project - Main business entity representing a construction contract.
      See ``construbot.proyectos.models.Contrato``

   Contraparte
      Counterparty or Business Partner - Client, subcontractor, or piecework contractor.
      See ``construbot.proyectos.models.Contraparte``

   Estimación
      Estimate or Progress Payment - Payment request for completed work.
      See ``construbot.proyectos.models.Estimate``

   Concepto
      Concept or Line Item - Individual work item in contract catalog.
      See ``construbot.proyectos.models.Concept``

   Retención
      Retention or Withholding - Financial withholding from payments.
      See ``construbot.proyectos.models.Retenciones``

   Sitio
      Site or Construction Site - Physical location where work is performed.
      See ``proyectos.models.Sitio``

   Destinatario
      Recipient or Contact - Person receiving documents or communications.
      See ``construbot.proyectos.models.Destinatario``

   Cliente
      Client - Type of Contraparte who hires the company.
      Choice value in ``Contraparte.tipo``

   Destajista
      Piecework Contractor - Type of Contraparte paid by completed work.
      Choice value in ``Contraparte.tipo``

   Subcontratista
      Subcontractor - Type of Contraparte performing specialized work.
      Choice value in ``Contraparte.tipo``

   folio
      Reference Number - Unique identifier for contracts within a company.
      Field in ``Contrato`` model

   monto
      Amount - Financial amount for contracts or estimates.
      Field in ``Contrato`` and ``Estimate`` models

   anticipo
      Advance Payment or Down Payment - Upfront payment before work begins.
      Field in ``Contrato`` model

See Also
========

- :doc:`/_glossary/domain-terms` - Complete glossary
- :doc:`/developer/architecture/multi-tenancy` - Architecture
- :doc:`/contributor/translation/glossary` - Translation guide
