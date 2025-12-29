============
Library Mode
============

Using Construbot as a Django app within your own project.

Overview
========

Construbot can run in two modes:

1. **Standalone Mode** (default) - Full application with admin, accounts, authentication
2. **Library Mode** - Django app embedded in your project

**Enable library mode:**

.. code-block:: bash

   CONSTRUBOT_AS_LIBRARY=True

What Changes
============

**When CONSTRUBOT_AS_LIBRARY=True:**

❌ **Disabled:**

- Django admin interface
- allauth URLs (account management)
- Standalone authentication views
- Account configuration app

✅ **Still Available:**

- Core business models (Contrato, Estimate, etc.)
- API endpoints
- Business logic and views (if you include URLs)
- Template tags and utilities

Use Cases
=========

**When to use library mode:**

- Integrating Construbot into existing Django project
- Using your own authentication system
- Customizing admin interface
- Building custom frontend

**When NOT to use:**

- Need complete standalone solution
- Want built-in authentication
- Using out-of-the-box

Setup
=====

**1. Install package:**

.. code-block:: bash

   pip install construbot  # When available on PyPI

   # Or from source:
   pip install git+https://github.com/javier-llamas/construbot.git

**2. Add to INSTALLED_APPS:**

.. code-block:: python

   INSTALLED_APPS = [
       # Your apps
       'myapp',

       # Add Construbot apps
       'construbot.users',
       'construbot.proyectos',
       'construbot.core',
       'construbot.api',

       # Django apps
       'django.contrib.admin',
       ...
   ]

**3. Set library mode:**

.. code-block:: bash

   # In .env
   CONSTRUBOT_AS_LIBRARY=True

**4. Include URLs (optional):**

.. code-block:: python

   # urls.py
   urlpatterns = [
       path('construbot/', include('construbot.proyectos.urls')),
       path('api/v1/', include('construbot.api.urls')),
   ]

**5. Run migrations:**

.. code-block:: bash

   python manage.py migrate

Configuration
=============

**Settings:**

.. code-block:: python

   # settings.py

   # Use Construbot's custom user model (recommended)
   AUTH_USER_MODEL = 'users.User'

   # Or map to your own user model
   # (requires custom integration)

   # Database
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           ...
       }
   }

   # Library mode
   CONSTRUBOT_AS_LIBRARY = True

Integration Patterns
====================

Using Construbot Models
-----------------------

.. code-block:: python

   from construbot.proyectos.models import Contrato, Contraparte
   from construbot.users.models import Company

   # Create company
   company = Company.objects.create(
       customer=my_customer,
       nombre="My Company"
   )

   # Create contract
   contract = Contrato.objects.create(
       company=company,
       folio="C-001",
       ...
   )

Custom Authentication
---------------------

.. code-block:: python

   # If not using Construbot's User model:
   # Map your users to Construbot companies

   from construbot.users.models import Company, UserCompany

   # Associate your user with Construbot company
   UserCompany.objects.create(
       user=my_user,  # Your user model
       company=construbot_company
   )

API Only
--------

.. code-block:: python

   # Use only Construbot's API, not web interface

   INSTALLED_APPS = [
       'construbot.users',
       'construbot.proyectos',
       'construbot.api',
       'rest_framework',
       'rest_framework_simplejwt',
   ]

   urlpatterns = [
       path('api/v1/', include('construbot.api.urls')),
   ]

Limitations
===========

**In library mode:**

- No built-in admin interface (use Django admin or build your own)
- No user registration/login views (implement your own)
- Manual setup required for permissions
- Need to handle company switching yourself

Troubleshooting
===============

**"No module named construbot":**

Ensure Construbot is installed:

.. code-block:: bash

   pip show construbot

**"Table doesn't exist":**

Run migrations:

.. code-block:: bash

   python manage.py migrate

**"AUTH_USER_MODEL conflicts":**

Choose one:

1. Use Construbot's User model: ``AUTH_USER_MODEL = 'users.User'``
2. Create custom integration between your User and Construbot models

Example Project
===============

.. code-block:: python

   # settings.py
   INSTALLED_APPS = [
       'myapp',
       'construbot.users',
       'construbot.proyectos',
       'construbot.core',
       'django.contrib.admin',
       ...
   ]

   AUTH_USER_MODEL = 'users.User'
   CONSTRUBOT_AS_LIBRARY = True

.. code-block:: python

   # urls.py
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('construbot/', include('construbot.proyectos.urls')),
       path('api/', include('construbot.api.urls')),
   ]

.. code-block:: python

   # views.py
   from construbot.proyectos.models import Contrato

   def my_view(request):
       contracts = Contrato.objects.filter(
           company=request.user.active_company
       )
       return render(request, 'my_template.html', {'contracts': contracts})

See Also
========

- :doc:`installation/index` - Development setup
- :doc:`architecture/overview` - Architecture details
- :doc:`api/index` - API documentation
