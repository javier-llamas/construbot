==========
Code Style
==========

Code style guidelines for Construbot contributions.

Python Style
============

Follow PEP 8
------------

**Code formatting:**

- 4 spaces for indentation (no tabs)
- Max line length: 100 characters (not strict 79)
- 2 blank lines between top-level functions/classes
- 1 blank line between methods

**Use Black:**

.. code-block:: bash

   black .

**Use isort:**

.. code-block:: bash

   isort .

Naming Conventions
------------------

.. code-block:: python

   # Variables and functions: snake_case
   user_count = 10
   def calculate_total():
       pass

   # Classes: PascalCase
   class ContractManager:
       pass

   # Constants: UPPER_CASE
   MAX_CONTRACTS = 100

   # Private: _leading_underscore
   def _internal_helper():
       pass

Type Hints
----------

**Encouraged but not required:**

.. code-block:: python

   def get_contracts(company: Company) -> QuerySet[Contrato]:
       return Contrato.objects.filter(company=company)

Docstrings
----------

**Use Google style:**

.. code-block:: python

   def create_contract(company, folio, amount):
       """Create a new contract.

       Args:
           company (Company): The company for this contract
           folio (str): Reference number
           amount (Decimal): Contract amount

       Returns:
           Contrato: The created contract

       Raises:
           ValidationError: If folio already exists
       """
       ...

Django Style
============

Model Best Practices
--------------------

**Always include company:**

.. code-block:: python

   class MyModel(models.Model):
       company = models.ForeignKey(Company, on_delete=models.CASCADE)

**Use verbose_name:**

.. code-block:: python

   class Contrato(models.Model):
       folio = models.CharField(
           max_length=100,
           verbose_name="Reference Number",
           help_text="Unique identifier for this contract"
       )

**Meta options:**

.. code-block:: python

   class Meta:
       ordering = ['-created_at']
       unique_together = ('company', 'folio')
       verbose_name_plural = "Contracts"

View Best Practices
-------------------

**Use class-based views:**

.. code-block:: python

   from django.views.generic import ListView

   class ContractListView(LoginRequiredMixin, ListView):
       model = Contrato
       template_name = 'contracts/list.html'

       def get_queryset(self):
           return Contrato.objects.filter(
               company=self.request.user.active_company
           )

**Always scope to company:**

.. code-block:: python

   # GOOD
   contracts = Contrato.objects.filter(company=request.user.active_company)

   # BAD
   contracts = Contrato.objects.all()  # Leaks data!

Query Optimization
------------------

**Use select_related:**

.. code-block:: python

   # Avoid N+1 queries
   contracts = Contrato.objects.select_related(
       'contraparte',
       'sitio'
   )

**Use prefetch_related:**

.. code-block:: python

   users = User.objects.prefetch_related('companies')

Security
========

**Never trust user input:**

.. code-block:: python

   # Use Django forms for validation
   form = ContractForm(request.POST)
   if form.is_valid():
       contract = form.save()

**Use get_object_or_404:**

.. code-block:: python

   contract = get_object_or_404(Contrato, id=contract_id)

**Check permissions:**

.. code-block:: python

   if not request.user.nivel_acceso.nivel >= 3:
       raise PermissionDenied()

Testing Style
=============

**Clear test names:**

.. code-block:: python

   def test_contract_creation_with_valid_data():
       pass

   def test_contract_creation_fails_with_duplicate_folio():
       pass

**Use setUp for common data:**

.. code-block:: python

   class ContractTestCase(TestCase):
       def setUp(self):
           self.company = Company.objects.create(...)

       def test_something(self):
           contract = Contrato.objects.create(company=self.company)

**One assertion per test (ideally):**

.. code-block:: python

   def test_contract_folio_is_uppercase(self):
       contract = Contrato.objects.create(folio="abc")
       self.assertEqual(contract.folio, "ABC")

Git Commit Messages
===================

**Format:**

.. code-block:: text

   Short summary (50 chars max)

   More detailed explanation if needed. Wrap at 72 characters.

   - List of changes
   - Another change

**Good examples:**

.. code-block:: text

   Add hierarchical contract support

   Implement django-treebeard for parent/child contract relationships.
   Includes migration, model updates, and tree query methods.

   Fix: Prevent data leak in contract list view

   Ensure contracts are filtered by active_company before display.

**Bad examples:**

.. code-block:: text

   Fixed stuff
   WIP
   asdf
   Updated code

Common Patterns
===============

**Factory pattern for tests:**

.. code-block:: python

   class ContractFactory:
       @staticmethod
       def create(**kwargs):
           defaults = {
               'company': CompanyFactory.create(),
               'folio': 'C-001',
               'monto': Decimal('1000000.00'),
           }
           defaults.update(kwargs)
           return Contrato.objects.create(**defaults)

**Context manager for transactions:**

.. code-block:: python

   from django.db import transaction

   with transaction.atomic():
       contract = Contrato.objects.create(...)
       estimate = Estimate.objects.create(contract=contract, ...)

**Queryset methods:**

.. code-block:: python

   class ContratoQuerySet(models.QuerySet):
       def for_company(self, company):
           return self.filter(company=company)

       def active(self):
           return self.filter(status='active')

Tools
=====

**Linting:**

.. code-block:: bash

   # pylint
   pylint construbot/

   # flake8
   flake8 construbot/

**Formatting:**

.. code-block:: bash

   # Black (code formatter)
   black .

   # isort (import sorting)
   isort .

**Type checking (optional):**

.. code-block:: bash

   mypy construbot/

Pre-commit Hooks
================

**Recommended .pre-commit-config.yaml:**

.. code-block:: yaml

   repos:
     - repo: https://github.com/psf/black
       rev: 22.10.0
       hooks:
         - id: black

     - repo: https://github.com/pycqa/isort
       rev: 5.10.1
       hooks:
         - id: isort

     - repo: https://github.com/pycqa/flake8
       rev: 5.0.4
       hooks:
         - id: flake8

See Also
========

- :doc:`getting-started` - Development setup
- :doc:`testing/index` - Testing guide
- `PEP 8 <https://pep8.org/>`_
- `Django Coding Style <https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/>`_
