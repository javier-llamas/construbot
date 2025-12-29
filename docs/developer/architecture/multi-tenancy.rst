==============
Multi-Tenancy
==============

Construbot's multi-tenant architecture with three-level hierarchy.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

Construbot uses a **three-level multi-tenant architecture**:

1. **Customer** - Top-level account (organization)
2. **Company** - Business entity within customer
3. **User** - Individual with access to one or more companies

**Data isolation:** All business data is scoped to Company level.

Hierarchy Structure
===================

.. code-block:: text

   Customer (Acme Corporation)
   ├── Company A (Acme Construction NY)
   │   ├── User: john@acme.com
   │   ├── User: jane@acme.com
   │   └── Data: Contracts, Estimates, etc.
   └── Company B (Acme Construction LA)
       ├── User: bob@acme.com
       ├── User: jane@acme.com (shared user)
       └── Data: Contracts, Estimates, etc.

**Key points:**

- Users can belong to multiple companies
- Data is never shared between companies
- Users switch between companies without re-login

Models
======

Customer Model
--------------

**File:** ``construbot/users/models.py``

.. code-block:: python

   class Customer(models.Model):
       """Top-level account/organization"""

       nombre = models.CharField(max_length=200)  # Name
       slug = models.SlugField(unique=True)
       activo = models.BooleanField(default=True)  # Active status
       created_at = models.DateTimeField(auto_now_add=True)

       def __str__(self):
           return self.nombre

**Purpose:**

- Group related companies
- Billing aggregation (if needed)
- Corporate-level reporting

Company Model
-------------

.. code-block:: python

   class Company(models.Model):
       """Business entity - main tenant unit"""

       customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
       nombre = models.CharField(max_length=200)
       slug = models.SlugField()
       activo = models.BooleanField(default=True)

       class Meta:
           unique_together = ('customer', 'slug')
           verbose_name_plural = 'Companies'

       def __str__(self):
           return self.nombre

**Purpose:**

- Primary tenant boundary
- All business data scoped here
- Separate operational entities

User Model
----------

.. code-block:: python

   class User(AbstractUser):
       """Custom user with multi-company support"""

       username = None  # Removed - using email
       email = models.EmailField(unique=True)

       # Multi-company relationships
       companies = models.ManyToManyField(
           Company,
           through='UserCompany',
           related_name='users'
       )

       # Current active company in session
       active_company = models.ForeignKey(
           Company,
           on_delete=models.SET_NULL,
           null=True,
           related_name='active_users'
       )

       # Permission level
       nivel_acceso = models.ForeignKey(
           'NivelAcceso',
           on_delete=models.PROTECT
       )

       USERNAME_FIELD = 'email'
       REQUIRED_FIELDS = []

UserCompany (Through Model)
----------------------------

.. code-block:: python

   class UserCompany(models.Model):
       """User-Company relationship with permissions"""

       user = models.ForeignKey(User, on_delete=models.CASCADE)
       company = models.ForeignKey(Company, on_delete=models.CASCADE)
       is_active = models.BooleanField(default=True)
       joined_at = models.DateTimeField(auto_now_add=True)

       class Meta:
           unique_together = ('user', 'company')

Data Isolation
==============

Company-Scoped Models
---------------------

**All business models include company foreign key:**

.. code-block:: python

   class Contrato(MP_Node):
       """Contract - main business entity"""

       company = models.ForeignKey(Company, on_delete=models.CASCADE)
       folio = models.CharField(max_length=100)
       # ... other fields

       class Meta:
           unique_together = ('company', 'folio')

**Other scoped models:**

- ``Contraparte`` (Counterparty)
- ``Sitio`` (Site)
- ``Estimate`` (Estimate)
- ``Concept`` (Line Item)
- ``Retenciones`` (Retention)

Querying with Company Filter
-----------------------------

**Always filter by company:**

.. code-block:: python

   # In views
   def contract_list(request):
       company = request.user.active_company
       contracts = Contrato.objects.filter(company=company)
       return render(request, 'contracts.html', {'contracts': contracts})

**Model manager (optional pattern):**

.. code-block:: python

   class CompanyQuerySet(models.QuerySet):
       def for_company(self, company):
           return self.filter(company=company)

   class Contrato(MP_Node):
       objects = CompanyQuerySet.as_manager()

       # Usage:
       # Contrato.objects.for_company(company)

Active Company Management
=========================

Setting Active Company
----------------------

**During login:**

.. code-block:: python

   def login_view(request):
       user = authenticate(email=email, password=password)
       if user:
           login(request, user)

           # Set active company (default to first)
           if not user.active_company:
               user.active_company = user.companies.first()
               user.save()

           return redirect('dashboard')

**Company switching:**

.. code-block:: python

   def switch_company(request, company_id):
       company = get_object_or_404(Company, id=company_id)

       # Verify user has access
       if company not in request.user.companies.all():
           return HttpResponseForbidden()

       # Switch active company
       request.user.active_company = company
       request.user.save()

       return redirect('dashboard')

Middleware (Optional)
---------------------

.. code-block:: python

   class ActiveCompanyMiddleware:
       """Ensure active_company is set"""

       def __init__(self, get_response):
           self.get_response = get_response

       def __call__(self, request):
           if request.user.is_authenticated:
               if not request.user.active_company:
                   # Set to first company or redirect to selection
                   request.user.active_company = request.user.companies.first()
                   request.user.save()

           return self.get_response(request)

Template Context
----------------

**Access in templates:**

.. code-block:: html+django

   <h1>{{ user.active_company.nombre }}</h1>

   {% if user.companies.count > 1 %}
       <select onchange="window.location=this.value">
           {% for company in user.companies.all %}
               <option value="{% url 'switch_company' company.id %}"
                       {% if company == user.active_company %}selected{% endif %}>
                   {{ company.nombre }}
               </option>
           {% endfor %}
       </select>
   {% endif %}

Multi-Company Forms
===================

Limit Choices to Current Company
---------------------------------

.. code-block:: python

   class ContratoForm(forms.ModelForm):
       class Meta:
           model = Contrato
           fields = ['contraparte', 'sitio', ...]

       def __init__(self, *args, company=None, **kwargs):
           super().__init__(*args, **kwargs)

           # Limit counterparties to current company
           if company:
               self.fields['contraparte'].queryset = \\
                   Contraparte.objects.filter(company=company)
               self.fields['sitio'].queryset = \\
                   Sitio.objects.filter(company=company)

**In views:**

.. code-block:: python

   def create_contract(request):
       if request.method == 'POST':
           form = ContratoForm(
               request.POST,
               company=request.user.active_company
           )
           if form.is_valid():
               contract = form.save(commit=False)
               contract.company = request.user.active_company
               contract.save()
       else:
           form = ContratoForm(company=request.user.active_company)

Admin Interface
===============

Company-Scoped Admin
--------------------

.. code-block:: python

   @admin.register(Contrato)
   class ContratoAdmin(admin.ModelAdmin):
       list_display = ['folio', 'company', 'contraparte']
       list_filter = ['company']

       def get_queryset(self, request):
           qs = super().get_queryset(request)

           # Superusers see all
           if request.user.is_superuser:
               return qs

           # Others see only their companies
           return qs.filter(company__in=request.user.companies.all())

       def save_model(self, request, obj, form, change):
           if not change:  # New object
               obj.company = request.user.active_company
           super().save_model(request, obj, form, change)

API Considerations
==================

Company from Token
------------------

.. code-block:: python

   from rest_framework.views import APIView

   class ContractListAPI(APIView):
       permission_classes = [IsAuthenticated]

       def get(self, request):
           company = request.user.active_company
           contracts = Contrato.objects.filter(company=company)
           serializer = ContratoSerializer(contracts, many=True)
           return Response(serializer.data)

Company Header (Alternative)
-----------------------------

.. code-block:: python

   # Client sends company ID in header
   # X-Company-ID: 123

   class CompanyFromHeaderMiddleware:
       def process_request(self, request):
           if request.user.is_authenticated:
               company_id = request.META.get('HTTP_X_COMPANY_ID')
               if company_id:
                   company = Company.objects.filter(
                       id=company_id,
                       users=request.user
                   ).first()
                   if company:
                       request.company = company

Best Practices
==============

**1. Always scope queries:**

.. code-block:: python

   # GOOD
   contracts = Contrato.objects.filter(company=request.user.active_company)

   # BAD - returns all companies' data!
   contracts = Contrato.objects.all()

**2. Validate company access:**

.. code-block:: python

   company = get_object_or_404(Company, id=company_id)
   if company not in request.user.companies.all():
       raise PermissionDenied

**3. Set company on create:**

.. code-block:: python

   contract = form.save(commit=False)
   contract.company = request.user.active_company  # Always set!
   contract.save()

**4. Use unique_together:**

.. code-block:: python

   class Meta:
       unique_together = ('company', 'folio')  # Unique per company

**5. Test data isolation:**

.. code-block:: python

   def test_company_isolation(self):
       company1 = Company.objects.create(name='Company 1')
       company2 = Company.objects.create(name='Company 2')

       contract1 = Contrato.objects.create(company=company1, ...)
       contract2 = Contrato.objects.create(company=company2, ...)

       # Should only see own company's data
       assert Contrato.objects.filter(company=company1).count() == 1

Common Patterns
===============

Company Context Manager
-----------------------

.. code-block:: python

   class CompanyMixin:
       """Mixin for company-scoped views"""

       def get_queryset(self):
           return super().get_queryset().filter(
               company=self.request.user.active_company
           )

       def form_valid(self, form):
           form.instance.company = self.request.user.active_company
           return super().form_valid(form)

**Usage:**

.. code-block:: python

   class ContractListView(CompanyMixin, ListView):
       model = Contrato

User Permission by Company
---------------------------

.. code-block:: python

   def has_company_permission(user, company, level=1):
       """Check if user has permission level for company"""
       if company not in user.companies.all():
           return False
       if user.nivel_acceso.nivel < level:
           return False
       return True

   # Usage:
   if not has_company_permission(request.user, company, level=3):
       raise PermissionDenied

Troubleshooting
===============

**User can't see data:**

- Check ``active_company`` is set
- Verify user is in company's users
- Confirm queries filter by ``company``

**Data leaking between companies:**

- Review querysets - must filter by ``company``
- Check forms limit choices to current company
- Verify ``unique_together`` includes ``company``

**Company switch not working:**

- Ensure ``active_company`` is saved
- Check session is persisting
- Verify user has access to target company

See Also
========

- :doc:`overview` - Architecture overview
- :doc:`authentication` - Authentication system
- :doc:`permission-levels` - Permission system
- :doc:`../models/users` - User model details
