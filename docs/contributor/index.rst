=================
Contributor Guide
=================

Welcome to the Construbot contributor documentation!

Overview
========

Thank you for your interest in contributing to Construbot! This guide covers everything you need to know about contributing code, documentation, translations, and more.

.. note::
   **First time contributor?** Start with :doc:`getting-started`

Ways to Contribute
===================

💻 **Code Contributions**

- Bug fixes
- New features
- Performance improvements
- Code refactoring

📚 **Documentation**

- Fix typos and errors
- Improve existing docs
- Add new guides
- Translate to Spanish

🌍 **Translations**

- Translate UI strings
- Update Spanish→English glossary
- Review translations

🐛 **Bug Reports**

- Report issues
- Provide reproduction steps
- Suggest fixes

✨ **Feature Requests**

- Propose new features
- Discuss improvements
- Vote on proposals

Quick Start
===========

**1. Fork and Clone:**

.. code-block:: bash

   # Fork on GitHub, then clone
   git clone https://github.com/YOUR-USERNAME/construbot.git
   cd construbot

**2. Set up development environment:**

.. code-block:: bash

   # Using Docker (recommended)
   make buildev

   # Or local setup
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements/local.txt

**3. Create feature branch:**

.. code-block:: bash

   git checkout -b feature/my-awesome-feature

**4. Make changes and test:**

.. code-block:: bash

   make test

**5. Submit pull request**

See :doc:`getting-started` for detailed steps.

Development Workflow
====================

**1. Find an issue or create one**

Browse https://github.com/javier-llamas/construbot/issues

**2. Discuss approach**

Comment on issue before starting major work

**3. Write code**

Follow :doc:`code-style` guidelines

**4. Write tests**

See :doc:`testing/index`

**5. Update documentation**

Document new features

**6. Submit PR**

Include clear description and tests

Code Style
==========

**Python:**

- Follow PEP 8
- Use Black for formatting
- Type hints encouraged
- Docstrings for public APIs

**Django:**

- Follow Django best practices
- Use Django's built-in features
- Company-scope all queries

See :doc:`code-style` for complete guidelines.

Testing
=======

**Run tests:**

.. code-block:: bash

   # Full test suite
   make test

   # Specific test
   pytest tests/test_models.py::test_contract_creation

   # With coverage
   make test
   open htmlcov/index.html

See :doc:`testing/index` for testing guide.

Documentation
=============

**Build docs:**

.. code-block:: bash

   cd docs
   make html
   open _build/html/index.rst

**Auto-rebuild:**

.. code-block:: bash

   make livehtml

See :doc:`documentation/index` for documentation guidelines.

Translation
===========

**Spanish→English glossary:**

See :doc:`translation/glossary` for complete term mappings.

**Add translations:**

.. code-block:: bash

   cd docs
   make update-translations
   # Edit locale/es/LC_MESSAGES/*.po

See :doc:`translation/index` for translation guide.

Pull Request Guidelines
========================

**Before submitting:**

✅ Tests pass (``make test``)

✅ Code follows style guide

✅ Documentation updated

✅ Commits are clear and atomic

✅ PR description explains changes

**PR template:**

.. code-block:: markdown

   ## Description
   Brief description of changes

   ## Motivation
   Why is this change needed?

   ## Changes
   - List of changes made

   ## Testing
   How was this tested?

   ## Screenshots (if applicable)

   ## Checklist
   - [ ] Tests pass
   - [ ] Documentation updated
   - [ ] Follows code style

Community
=========

**Be respectful and inclusive**

We follow the Contributor Covenant Code of Conduct.

**Ask for help**

- GitHub Issues
- GitHub Discussions (if available)

**Give feedback**

Your input helps improve Construbot!

Documentation Sections
======================

.. toctree::
   :maxdepth: 2

   getting-started
   code-style
   testing/index
   translation/glossary
   documentation/index

Resources
=========

- **GitHub:** https://github.com/javier-llamas/construbot
- **Issues:** https://github.com/javier-llamas/construbot/issues
- **Developer Docs:** :doc:`/developer/index`
- **Architecture:** :doc:`/developer/architecture/index`

License
=======

By contributing, you agree that your contributions will be licensed under the AGPLv3 license.

Thank You
=========

Thank you for contributing to Construbot! Your contributions help make this project better for everyone.
