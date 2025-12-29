=============
Documentation
=============

Guide for contributing to Construbot documentation.

Overview
========

Construbot documentation uses Sphinx with reStructuredText (RST) and supports bilingual builds (English/Spanish).

**Location:** ``/docs/``

Building Documentation
======================

**Build English docs:**

.. code-block:: bash

   cd docs
   make html
   open _build/html/index.html

**Build Spanish docs:**

.. code-block:: bash

   make html-es
   open _build/html/es/index.html

**Auto-rebuild (live preview):**

.. code-block:: bash

   make livehtml
   # Opens http://127.0.0.1:8000

Writing Documentation
=====================

**RST Syntax:**

.. code-block:: rst

   ==============
   Page Title
   ==============

   Section
   =======

   Subsection
   ----------

   **Bold text**
   *Italic text*
   ``Code inline``

   .. code-block:: python

      # Code block
      def example():
          pass

   .. note::
      Admonition block

**Links:**

.. code-block:: rst

   :doc:`other-page`
   :doc:`/full/path/to/page`
   `External link <https://example.com>`_

**Cross-references:**

.. code-block:: rst

   See :doc:`../architecture/overview`
   See :class:`construbot.proyectos.models.Contrato`

Documentation Structure
=======================

.. code-block:: text

   docs/
   ├── index.rst (main entry point)
   ├── user-guide/
   ├── developer/
   ├── contributor/
   ├── reference/
   └── _glossary/

**Follow existing structure** when adding new pages.

Style Guide
===========

**1. Clear and concise**

**2. Code examples**

Include working code examples.

**3. Spanish terms**

Use pattern: "Contracts (Spanish: Contratos)"

**4. Cross-references**

Link to related pages.

**5. Consistent formatting**

Follow existing page structure.

Translation Workflow
====================

**Extract strings:**

.. code-block:: bash

   cd docs
   make gettext

**Update translations:**

.. code-block:: bash

   make update-translations

**Edit .po files:**

.. code-block:: bash

   # Edit locale/es/LC_MESSAGES/*.po
   nano locale/es/LC_MESSAGES/index.po

**Build Spanish version:**

.. code-block:: bash

   make html-es

See Also
========

- :doc:`../getting-started` - Contributor setup
- :doc:`../translation/glossary` - Translation guide
- :doc:`/reference/glossary` - Spanish→English terms
