==================
Permission Levels
==================

Six-tier permission system (NIVELES_ACCESO) for access control.

Overview
========

**Six permission levels:**

1. **Auxiliar** (1) - View only
2. **Coordinador** (2) - Create and edit
3. **Director** (3) - Full CRUD operations
4. **Corporativo** (4) - Cross-company access
5. **Soporte** (5) - Support/maintenance
6. **Superusuario** (6) - Full system access

**Implementation:** Foreign key on User model pointing to NivelAcceso.

NivelAcceso Model
=================

**File:** ``construbot/users/models.py``

.. code-block:: python

   class NivelAcceso(models.Model):
       """Permission level definition"""

       nombre = models.CharField(max_length=50)  # Name
       nivel = models.IntegerField(unique=True)  # Level number (1-6)
       descripcion = models.TextField(blank=True)

       class Meta:
           ordering = ['nivel']
           verbose_name_plural = 'Niveles de Acceso'

       def __str__(self):
           return f"{self.nivel} - {self.nombre}"

**Default levels:**

.. code-block:: python

   # Populated via migration or fixtures
   1 - Auxiliar
   2 - Coordinador
   3 - Director
   4 - Corporativo
   5 - Soporte
   6 - Superusuario

User Assignment
===============

.. code-block:: python

   class User(AbstractUser):
       nivel_acceso = models.ForeignKey(
           NivelAcceso,
           on_delete=models.PROTECT,
           related_name='users'
       )

**Setting level:**

.. code-block:: python

   user = User.objects.get(email='user@example.com')
   user.nivel_acceso = NivelAcceso.objects.get(nivel=3)  # Director
   user.save()

Permission Checks
=================

View Decorators
---------------

.. code-block:: python

   def nivel_required(min_level):
       """Decorator to require minimum permission level"""
       def decorator(view_func):
           @wraps(view_func)
           def wrapper(request, *args, **kwargs):
               if not request.user.is_authenticated:
                   return redirect('login')
               if request.user.nivel_acceso.nivel < min_level:
                   raise PermissionDenied(f"Requires level {min_level}")
               return view_func(request, *args, **kwargs)
           return wrapper
       return decorator

   # Usage
   @nivel_required(3)  # Director or higher
   def delete_contract(request, contract_id):
       ...

Class-Based Views
-----------------

.. code-block:: python

   class NivelRequiredMixin:
       """Mixin for permission level check"""
       required_nivel = 1  # Override in subclass

       def dispatch(self, request, *args, **kwargs):
           if request.user.nivel_acceso.nivel < self.required_nivel:
               raise PermissionDenied()
           return super().dispatch(request, *args, **kwargs)

   class ContractDeleteView(NivelRequiredMixin, DeleteView):
       required_nivel = 3  # Director
       model = Contrato

Template Checks
---------------

.. code-block:: html+django

   {% if user.nivel_acceso.nivel >= 3 %}
       <a href="{% url 'delete_contract' contract.id %}">Delete</a>
   {% endif %}

   {% if user.nivel_acceso.nivel == 6 %}
       <div class="admin-panel">...</div>
   {% endif %}

Level-Specific Capabilities
============================

1. Auxiliar (View Only)
------------------------

**Permissions:**

- View contracts, estimates, reports
- No create/edit/delete

**Use case:** Field workers, read-only access

.. code-block:: python

   @nivel_required(1)
   def view_contract(request, contract_id):
       # Can view but not edit

2. Coordinador (Create/Edit)
-----------------------------

**Permissions:**

- All Auxiliar permissions
- Create new records
- Edit existing records
- Cannot delete

**Use case:** Project coordinators

.. code-block:: python

   @nivel_required(2)
   def create_estimate(request):
       # Can create estimates

3. Director (Full CRUD)
-----------------------

**Permissions:**

- All Coordinador permissions
- Delete records
- Approve estimates
- Generate reports

**Use case:** Project managers, directors

.. code-block:: python

   @nivel_required(3)
   def delete_contract(request, contract_id):
       # Can delete contracts

4. Corporativo (Multi-Company)
-------------------------------

**Permissions:**

- All Director permissions
- Access multiple companies
- Cross-company reports
- Company-level configuration

**Use case:** Corporate-level management

.. code-block:: python

   @nivel_required(4)
   def corporate_report(request):
       # Access all companies under customer
       companies = Company.objects.filter(customer=request.user.customer)

5. Soporte (Support Access)
----------------------------

**Permissions:**

- Technical support access
- System diagnostics
- User assistance
- Limited configuration

**Use case:** Technical support staff

.. code-block:: python

   @nivel_required(5)
   def system_diagnostics(request):
       # Support-only features

6. Superusuario (Full Access)
------------------------------

**Permissions:**

- All system access
- Django admin
- User management
- System configuration

**Use case:** System administrators

.. code-block:: python

   # Django superuser check
   if request.user.is_superuser:
       # Full access

Combining with Company Scope
=============================

**Always combine level check with company scope:**

.. code-block:: python

   @login_required
   @nivel_required(2)
   def create_contract(request):
       # Level check passed
       company = request.user.active_company

       if request.method == 'POST':
           contract = form.save(commit=False)
           contract.company = company  # Company scope
           contract.save()

API Permissions
===============

.. code-block:: python

   from rest_framework.permissions import BasePermission

   class HasNivelAcceso(BasePermission):
       """DRF permission for nivel check"""

       def has_permission(self, request, view):
           required_level = getattr(view, 'required_nivel', 1)
           return request.user.nivel_acceso.nivel >= required_level

   # Usage
   class ContractViewSet(viewsets.ModelViewSet):
       required_nivel = 3
       permission_classes = [IsAuthenticated, HasNivelAcceso]

Best Practices
==============

**1. Use minimum required level:**

.. code-block:: python

   # GOOD - requires minimum needed
   @nivel_required(2)
   def edit_view(request):
       ...

   # BAD - unnecessarily restrictive
   @nivel_required(6)  # Unless truly needed

**2. Check in views, not templates:**

.. code-block:: python

   # GOOD - security in view
   @nivel_required(3)
   def delete_view(request):
       ...

   # BAD - relying only on template hiding
   # <a href="delete">Delete</a>  (no view protection)

**3. Combine checks:**

.. code-block:: python

   @login_required
   @nivel_required(3)
   def delete_contract(request, contract_id):
       contract = get_object_or_404(Contrato, id=contract_id)

       # Also verify company access
       if contract.company != request.user.active_company:
           raise PermissionDenied()

       contract.delete()

**4. Document required levels:**

.. code-block:: python

   @nivel_required(3)
   def delete_contract(request, contract_id):
       """
       Delete a contract.

       Requires: Director level (3) or higher
       """

Troubleshooting
===============

**PermissionDenied errors:**

- Check user's nivel_acceso level
- Verify required level is correct
- Confirm user is authenticated

**User can't access feature:**

- Check nivel_acceso assignment
- Verify permission decorator is applied
- Confirm level threshold is appropriate

See Also
========

- :doc:`authentication` - Authentication system
- :doc:`multi-tenancy` - Multi-company architecture
- :doc:`../models/users` - User model reference
