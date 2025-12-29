==========================
Domain Terms Glossary
==========================

This glossary maps Spanish construction industry terms used in Construbot to their English equivalents.
Use this for consistency in all documentation, translations, and communication.

.. note::
   **Important**: The codebase uses Spanish model and field names. This glossary provides English
   equivalents for documentation purposes only. Do not change the actual Python code to use these
   English names.

Core Entities
=============

.. glossary::
   :sorted:

   Contrato
      **English:** Contract / Project

      **Description:** A construction project or contract. Represents the main entity in Construbot for managing
      construction work. Can be hierarchical (parent contracts with sub-contracts) using django-treebeard.

      **Model:** ``construbot.proyectos.models.Contrato``

      **Key Fields:** folio (reference number), contrato_name (contract name), monto (amount), anticipo (advance payment)

      **Examples:** "Main Building Contract", "Electrical Subcontract"

   Contraparte
      **English:** Counterparty / Business Partner

      **Description:** An external business entity with which your company has a relationship. Can be one of three types:
      Cliente (Client), Destajista (Piecework Contractor), or Subcontratista (Subcontractor).

      **Model:** ``construbot.proyectos.models.Contraparte``

      **Types:** CLIENTE, DESTAJISTA, SUBCONTRATISTA

      **Examples:** "ABC Construction Inc. (Client)", "XYZ Electrical (Subcontractor)"

   Cliente
      **English:** Client / Customer

      **Description:** A customer who contracts construction work from your company. This is a Contraparte with tipo='CLIENTE'.

      **Model:** ``construbot.proyectos.models.Contraparte`` (tipo='CLIENTE')

      **Usage:** The party paying for the construction work

      **Examples:** "Government Agency", "Private Developer"

   Destajista
      **English:** Piecework Contractor / Task Contractor

      **Description:** A contractor paid by completed work units (piece rate) rather than by time. This is a Contraparte
      with tipo='DESTAJISTA'. Common in Mexican construction industry.

      **Model:** ``construbot.proyectos.models.Contraparte`` (tipo='DESTAJISTA')

      **Usage:** Workers paid per completed task or quantity

      **Examples:** "Masonry crew paid per square meter", "Painting contractor paid per room"

   Subcontratista
      **English:** Subcontractor

      **Description:** A contractor for specialized work under a main contract. This is a Contraparte with tipo='SUBCONTRATISTA'.

      **Model:** ``construbot.proyectos.models.Contraparte`` (tipo='SUBCONTRATISTA')

      **Usage:** Specialized contractors (electrical, plumbing, HVAC, etc.)

      **Examples:** "HVAC Subcontractor", "Structural Steel Subcontractor"

   Sitio
      **English:** Site / Construction Site / Location

      **Description:** Physical location where construction work occurs. Must be associated with a Cliente (Client) contraparte.

      **Model:** ``construbot.proyectos.models.Sitio``

      **Key Fields:** sitio_name (site name), sitio_location (address), cliente (associated client)

      **Examples:** "Downtown Office Building", "Highway 101 Bridge Project"

   Destinatario
      **English:** Recipient / Contact / Contact Person

      **Description:** A contact person at a Counterparty organization. Used for document distribution and communication.

      **Model:** ``construbot.proyectos.models.Destinatario``

      **Key Fields:** destinatario_text (contact name), puesto (position), contraparte (associated counterparty)

      **Examples:** "John Doe, Project Manager", "Jane Smith, Procurement Officer"

Financial Terms
===============

.. glossary::
   :sorted:

   Estimación
      **English:** Estimate / Progress Payment / Progress Billing

      **Description:** Periodic billing for completed work on a contract. Documents work progress and calculates payment due.

      **Model:** ``construbot.proyectos.models.Estimate``

      **Key Fields:** consecutive (estimate number), start_date, finish_date, project (associated contract)

      **Examples:** "Estimate #5 for March 2024", "Monthly Progress Payment"

   Concepto
      **English:** Concept / Line Item / Work Item / Work Package

      **Description:** Individual work item in a contract catalog. Defines a specific type of work with quantity,
      unit of measurement, and unit price.

      **Model:** ``construbot.proyectos.models.Concept``

      **Key Fields:** code (item code), concept_text (description), unit (measurement unit), unit_price, total_cuantity

      **Examples:** "Concrete Pouring - Foundation", "Electrical Wiring Installation"

   Retención
      **English:** Retention / Withholding / Holdback

      **Description:** Amount or percentage withheld from payments, typically released upon project completion.
      Can be a fixed amount (AMOUNT) or percentage (PERCENTAGE).

      **Model:** ``construbot.proyectos.models.Retenciones``

      **Types:** AMOUNT (Monto), PERCENTAGE (Porcentaje)

      **Examples:** "5% Quality Retention", "$10,000 Performance Holdback"

   Anticipo
      **English:** Advance Payment / Down Payment / Mobilization Payment

      **Description:** Initial payment percentage for a contract, typically used for mobilization and initial expenses.

      **Model Field:** ``construbot.proyectos.models.Contrato.anticipo`` (DecimalField)

      **Range:** 0% to 100%

      **Examples:** "10% advance payment", "15% mobilization payment"

   Monto
      **English:** Amount / Total Amount / Contract Amount

      **Description:** Total monetary value of a contract or payment. Usually specified without VAT/IVA.

      **Model Fields:** ``Contrato.monto``, ``Retenciones.valor``

      **Examples:** "$1,000,000 contract amount", "$50,000 retention amount"

   Amortización
      **English:** Amortization / Advance Amortization

      **Description:** The process of deducting advance payment amounts from subsequent progress payments.

      **Method:** ``Contrato.amortizacion_anticipo()``

      **Usage:** Calculated automatically in estimates to recover advance payments

   Ejercido
      **English:** Executed / Spent / Expended

      **Description:** Amount of work completed or money spent to date.

      **Method:** ``Contrato.ejercido_acumulado()``

      **Examples:** "Accumulated executed amount", "Total spent to date"

   Facturado
      **English:** Invoiced / Billed

      **Description:** Indicates whether an estimate has been invoiced to the client.

      **Model Field:** ``Estimate.invoiced`` (BooleanField)

   Pagado
      **English:** Paid / Payment Completed

      **Description:** Indicates whether an estimate payment has been received.

      **Model Fields:** ``Estimate.paid`` (BooleanField), ``Estimate.payment_date`` (DateField)

Field Names
===========

.. glossary::
   :sorted:

   folio
      **English:** Reference Number / Folio / Sequential ID

      **Description:** Sequential identification number for contracts within a company.

      **Model Field:** ``Contrato.folio`` (IntegerField)

   fecha
      **English:** Date / Contract Date

      **Description:** Date of contract signing or creation.

      **Model Field:** ``Contrato.fecha`` (DateField)

   nombre
      **English:** Name

      **Description:** Generic name field used across multiple models.

      **Model Fields:** ``Vertices.nombre``, ``Retenciones.nombre``

   puesto
      **English:** Position / Job Title / Role

      **Description:** Job title or position of a person.

      **Model Fields:** ``Destinatario.puesto``, ``User.puesto``

      **Examples:** "Project Manager", "Site Supervisor", "Procurement Officer"

   code
      **English:** Code / Item Code / Contract Code

      **Description:** Alphanumeric code for identification.

      **Model Fields:** ``Contrato.code``, ``Concept.code``

      **Examples:** "CONT-2024-001", "ELEC-100"

   valor
      **English:** Value / Amount

      **Description:** Monetary or numeric value.

      **Model Field:** ``Retenciones.valor`` (DecimalField)

   tipo
      **English:** Type / Category

      **Description:** Classification or type field with choices.

      **Model Fields:** ``Contraparte.tipo``, ``Retenciones.tipo``

Measurement & Quantity Terms
=============================

.. glossary::
   :sorted:

   Unidad
      **English:** Unit / Unit of Measurement / Measurement Unit

      **Description:** Unit for measuring work quantities (square meters, kilograms, pieces, etc.)

      **Model:** ``construbot.proyectos.models.Units``

      **Examples:** "m²" (square meters), "kg" (kilograms), "pza" (pieces), "m³" (cubic meters)

   Cantidad
      **English:** Quantity / Amount

      **Description:** Numeric quantity of work or materials.

      **Model Fields:** ``Concept.total_cuantity``, ``EstimateConcept.cuantity_estimated``

   Vértice
      **English:** Vertex / Measurement Point / Survey Point

      **Description:** A point used for calculating quantities with dimensions (length, width, height).

      **Model:** ``construbot.proyectos.models.Vertices``

      **Key Fields:** nombre (name), largo (length), ancho (width), alto (height), piezas (pieces)

   largo
      **English:** Length / Long

      **Description:** Length dimension in meters.

      **Model Field:** ``Vertices.largo`` (DecimalField)

   ancho
      **English:** Width / Wide

      **Description:** Width dimension in meters.

      **Model Field:** ``Vertices.ancho`` (DecimalField)

   alto
      **English:** Height / Tall / High

      **Description:** Height dimension in meters.

      **Model Field:** ``Vertices.alto`` (DecimalField)

   piezas
      **English:** Pieces / Number of Pieces / Count

      **Description:** Count or number of identical items.

      **Model Field:** ``Vertices.piezas`` (IntegerField)

Organizational Terms
====================

.. glossary::
   :sorted:

   Empresa
      **English:** Company / Business Entity

      **Description:** Business entity within a Customer account in the multi-tenant system.

      **Model:** ``construbot.users.models.Company``

      **Hierarchy:** Customer → Company → User

   Cliente (Sistema)
      **English:** Customer / Account / Tenant

      **Description:** Top-level organization account in the multi-tenant system. Not to be confused with
      Cliente (Client) in Contraparte.

      **Model:** ``construbot.users.models.Customer``

      **Hierarchy:** Customer → Company → User

   Usuario
      **English:** User

      **Description:** System user with permissions and company assignments.

      **Model:** ``construbot.users.models.User``

      **Key Fields:** email (authentication), company (assigned companies), permiso (permission level)

   Nivel de Acceso
      **English:** Access Level / Permission Level

      **Description:** User permission level (1-6).

      **Model:** ``construbot.users.models.NivelAcceso``

      **Levels:**

      - 1: Auxiliar (Assistant)
      - 2: Coordinador (Coordinator)
      - 3: Director (Director)
      - 4: Corporativo (Corporate)
      - 5: Soporte (Support)
      - 6: Superusuario (Superuser)

Action Terms
============

.. glossary::
   :sorted:

   Supervisado por
      **English:** Supervised By / Overseen By

      **Description:** User who supervised or managed the work.

      **Model Field:** ``Estimate.supervised_by`` (ForeignKey to User)

   Autorizado por
      **English:** Authorized By / Approved By

      **Description:** Person who authorized or approved a document.

      **Model Fields:** ``Estimate.auth_by``, ``Estimate.auth_by_gen``

   Elaborado por
      **English:** Drafted By / Prepared By / Created By

      **Description:** User who created or drafted a document.

      **Model Field:** ``Estimate.draft_by`` (ForeignKey to User)

   Asignar
      **English:** Assign / Allocate

      **Description:** Action of assigning users or resources to a contract.

      **Model Field:** ``Contrato.users`` (ManyToManyField)

Documentation & UI Terms
========================

.. glossary::
   :sorted:

   Catálogo
      **English:** Catalog / Price Book / Work Item List

      **Description:** List or catalog of work items (concepts) for a contract.

      **Usage:** "Concept Catalog", "Price Catalog"

   Generador
      **English:** Generator / Estimate Generator

      **Description:** The estimate generation document or system.

      **Usage:** Authorization field for estimates (auth_by_gen)

   Observaciones
      **English:** Observations / Notes / Comments

      **Description:** Free-text notes or comments on items.

      **Model Field:** ``EstimateConcept.observations`` (TextField)

   Consecutivo
      **English:** Consecutive / Sequential Number / Estimate Number

      **Description:** Sequential numbering for estimates within a project.

      **Model Field:** ``Estimate.consecutive`` (IntegerField)

   Ubicación
      **English:** Location / Address / Site Location

      **Description:** Physical address or location description.

      **Model Field:** ``Sitio.sitio_location`` (CharField)

Status & State Terms
====================

.. glossary::
   :sorted:

   Vigente
      **English:** Active / Current / Ongoing

      **Description:** Indicates an active or ongoing contract.

      **Model Field:** ``Contrato.status`` (BooleanField)

      **Function:** ``contratosvigentes()`` - Returns active contracts

   Pendiente
      **English:** Pending / Outstanding / Awaiting

      **Description:** Items awaiting action (payment, invoicing, etc.)

      **Functions:** ``estimacionespendientes_facturacion()``, ``estimacionespendientes_pago()``

   Completado
      **English:** Completed / Finished / Done

      **Description:** Work or action that has been completed.

Translation Guidelines
======================

Model Names in Code
-------------------

**Keep Spanish names in Python code**, use English in documentation:

- Python: ``class Contrato(MP_Node):``
- Documentation: "The Contract model represents..."

**First Use Pattern**: On first use in any document, include Spanish term:

   "The Contract (Contrato) model represents construction projects..."

Field Names in Documentation
-----------------------------

**Reference both names** when documenting fields:

   "The ``folio`` (reference number) field stores the sequential contract ID..."

API Response Documentation
--------------------------

**Document JSON keys** with both languages:

.. code-block:: json

   {
     "folio": 1,           // Reference Number
     "monto": 1000000.00,  // Amount
     "anticipo": 10.00     // Advance Payment %
   }

Choice Field Values
-------------------

**Document all options** in tables:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Spanish Code
     - English Translation
     - Description
   * - CLIENTE
     - Client
     - Customer paying for work
   * - DESTAJISTA
     - Piecework Contractor
     - Worker paid by task
   * - SUBCONTRATISTA
     - Subcontractor
     - Specialized contractor

Consistency Rules
-----------------

1. **Always use the same English term** for a Spanish term across all documentation
2. **Provide context** when terms could be ambiguous
3. **Link to models** for technical reference
4. **Use industry-standard English** construction terminology where applicable
5. **Update this glossary** when adding new Spanish terms to the codebase

Usage in Different Contexts
============================

End User Documentation
----------------------

Use **plain English with Spanish reference on first use**:

   "To create a new Project (Contrato), navigate to the Projects menu..."

Developer Documentation
-----------------------

Use **both names with model references**:

   "The ``Contrato`` (Contract) model inherits from ``MP_Node`` for hierarchical structure.
   The ``monto`` (amount) field stores the contract value..."

API Documentation
-----------------

Use **English descriptions with Spanish field names**:

   **folio** (integer): Reference number / Sequential ID for the contract

See Also
========

* :doc:`/reference/glossary` - User-facing glossary
* :doc:`/contributor/translation/glossary` - Full contributor glossary
* :doc:`/developer/models/proyectos` - Model documentation
* :doc:`/user-guide/concepts/index` - Concept explanations for end users

---

**Last Updated:** December 2025

**Note:** This glossary is a living document. When adding new Spanish terms to the codebase,
update this glossary with the appropriate English translation and context.
