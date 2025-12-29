=======
Testing
=======

Testing guide for Construbot contributors.

Running Tests
=============

**Full test suite:**

.. code-block:: bash

   make test

**Specific tests:**

.. code-block:: bash

   # Specific file
   pytest tests/test_models.py

   # Specific test
   pytest tests/test_models.py::test_contract_creation

   # Tagged tests
   make current  # Runs tests with @tag('current')

**With coverage:**

.. code-block:: bash

   make test
   open htmlcov/index.html

Writing Tests
=============

**Test structure:**

.. code-block:: python

   from django.test import TestCase
   from construbot.proyectos.models import Contrato

   class ContratoTestCase(TestCase):
       def setUp(self):
           self.company = Company.objects.create(...)

       def test_contract_creation(self):
           contract = Contrato.objects.create(
               company=self.company,
               folio="C-001"
           )
           self.assertEqual(contract.folio, "C-001")

**Use factories:**

.. code-block:: python

   from tests.factories import ContractFactory

   contract = ContractFactory(company=self.company)

Best Practices
==============

✅ Test one thing per test

✅ Use descriptive test names

✅ Isolate tests (don't depend on other tests)

✅ Use fixtures for common setup

✅ Tag work-in-progress tests with ``@tag('current')``

Test Coverage
=============

**Target:** >80% coverage

**Check coverage:**

.. code-block:: bash

   make test
   coverage report

See Also
========

- :doc:`../getting-started` - Development setup
- :doc:`/developer/installation/index` - Installation guide
