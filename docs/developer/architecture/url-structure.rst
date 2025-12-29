==============
URL Structure
==============

URL routing and organization in Construbot.

Root URLs
=========

**File:** ``construbot/config/urls.py``

.. code-block:: python

   urlpatterns = [
       path('', UserRedirectView.as_view(), name='home'),
       path('admin/', admin.site.urls),
       path('accounts/', include('allauth.urls')),
       path('users/', include('construbot.users.urls', namespace='users')),
       path('proyectos/', include('construbot.proyectos.urls', namespace='proyectos')),
       path('core/', include('construbot.core.urls', namespace='core')),
       path('api/v1/', include('construbot.api.urls')),
   ]

**Library mode:**

.. code-block:: python

   if not settings.CONSTRUBOT_AS_LIBRARY:
       urlpatterns += [
           path('admin/', admin.site.urls),
           path('accounts/', include('allauth.urls')),
       ]

URL Patterns by App
===================

Users App
---------

**``/users/``** - User management

- ``/users/~redirect/`` - Redirect to user detail
- ``/users/~update/`` - Update user profile
- ``/users/<username>/`` - User detail

Proyectos App
-------------

**``/proyectos/``** - Main business logic

- ``/proyectos/contratos/`` - Contract list
- ``/proyectos/contratos/create/`` - Create contract
- ``/proyectos/contratos/<id>/`` - Contract detail
- ``/proyectos/contratos/<id>/edit/`` - Edit contract
- ``/proyectos/contratos/<id>/delete/`` - Delete contract
- ``/proyectos/estimaciones/`` - Estimate list
- ``/proyectos/contrapartes/`` - Counterparty list

API URLs
--------

**``/api/v1/``** - REST API

- ``/api/v1/api-token-auth/`` - Obtain JWT token
- ``/api/v1/api-token-refresh/`` - Refresh JWT token
- ``/api/v1/contracts/`` - Contract endpoints
- ``/api/v1/estimates/`` - Estimate endpoints

URL Namespaces
==============

**Using namespaces:**

.. code-block:: python

   # In templates
   {% url 'proyectos:contract_list' %}
   {% url 'users:detail' username=user.username %}

   # In views
   reverse('proyectos:contract_detail', kwargs={'pk': contract.id})

Admin URLs
==========

**``/admin/``** - Django admin (if not library mode)

Autocomplete URLs
=================

**django-autocomplete-light:**

.. code-block:: python

   urlpatterns = [
       path('autocomplete/', include('dal.urls')),
   ]

Static/Media URLs
=================

**Development only:**

.. code-block:: python

   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

**Production:** Served by WhiteNoise (static) and Nginx/S3 (media)

See Also
========

- :doc:`overview` - Architecture overview
- :doc:`../api/index` - API documentation
