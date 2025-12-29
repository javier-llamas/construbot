==============
Authentication
==============

Email-based authentication system with multi-company support.

Overview
========

**Key features:**

- Email as username (no separate username field)
- Custom authentication backend
- Multi-company access without re-login
- django-allauth integration
- JWT tokens for API

**Models:**

- Custom User model (``users.User``)
- Session-based for web
- JWT for API

Custom User Model
=================

**AUTH_USER_MODEL:** ``users.User``

.. code-block:: python

   class User(AbstractUser):
       username = None  # Removed
       email = models.EmailField(unique=True)

       companies = models.ManyToManyField(Company)
       active_company = models.ForeignKey(Company, null=True)
       nivel_acceso = models.ForeignKey(NivelAcceso)

       USERNAME_FIELD = 'email'
       REQUIRED_FIELDS = []

**Settings:**

.. code-block:: python

   # construbot/config/settings/base.py
   AUTH_USER_MODEL = 'users.User'

   AUTHENTICATION_BACKENDS = [
       'construbot.core.backends.ModelBackend',  # Custom
       'allauth.account.auth_backends.AuthenticationBackend',
   ]

Authentication Backend
======================

**File:** ``construbot/core/backends.py``

.. code-block:: python

   from django.contrib.auth.backends import ModelBackend as DjangoModelBackend

   class ModelBackend(DjangoModelBackend):
       """Custom backend for email authentication"""

       def authenticate(self, request, username=None, password=None, **kwargs):
           # Email passed as 'username' parameter
           email = kwargs.get('email', username)

           try:
               user = User.objects.get(email=email)
           except User.DoesNotExist:
               return None

           if user.check_password(password):
               return user
           return None

       def get_user(self, user_id):
           try:
               return User.objects.get(pk=user_id)
           except User.DoesNotExist:
               return None

Web Authentication
==================

Login View
----------

.. code-block:: python

   from django.contrib.auth import authenticate, login

   def login_view(request):
       if request.method == 'POST':
           email = request.POST.get('email')
           password = request.POST.get('password')

           user = authenticate(request, email=email, password=password)

           if user is not None:
               login(request, user)

               # Set active company
               if not user.active_company and user.companies.exists():
                   user.active_company = user.companies.first()
                   user.save()

               return redirect('dashboard')
           else:
               messages.error(request, 'Invalid credentials')

       return render(request, 'account/login.html')

Session Management
------------------

**Sessions stored in:**

- Database (default): ``django.contrib.sessions.backends.db``
- Cache (faster): ``django.contrib.sessions.backends.cache``
- Cached DB (recommended): ``django.contrib.sessions.backends.cached_db``

**Settings:**

.. code-block:: python

   # Production recommended
   SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
   SESSION_COOKIE_AGE = 1209600  # 2 weeks
   SESSION_COOKIE_SECURE = True  # HTTPS only
   SESSION_COOKIE_HTTPONLY = True  # No JavaScript access

Company Context in Session
---------------------------

.. code-block:: python

   # After login, active_company stored in User model
   request.user.active_company  # Current company

   # Switch company
   def switch_company(request, company_id):
       company = get_object_or_404(Company, id=company_id)
       if company in request.user.companies.all():
           request.user.active_company = company
           request.user.save()
       return redirect('dashboard')

django-allauth Integration
===========================

**Configuration:**

.. code-block:: python

   INSTALLED_APPS = [
       'allauth',
       'allauth.account',
       'allauth.socialaccount',  # Optional
   ]

   # Allauth settings
   ACCOUNT_AUTHENTICATION_METHOD = 'email'
   ACCOUNT_EMAIL_REQUIRED = True
   ACCOUNT_USERNAME_REQUIRED = False
   ACCOUNT_USER_MODEL_USERNAME_FIELD = None

**URLs:**

.. code-block:: python

   urlpatterns = [
       path('accounts/', include('allauth.urls')),
   ]

**Templates:**

Override allauth templates in ``templates/account/``:

- ``login.html``
- ``signup.html``
- ``password_reset.html``

API Authentication
==================

JWT Configuration
-----------------

**Packages:**

- ``djangorestframework``
- ``djangorestframework-simplejwt``

**Settings:**

.. code-block:: python

   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework_simplejwt.authentication.JWTAuthentication',
       ],
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
   }

   from datetime import timedelta

   SIMPLE_JWT = {
       'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
       'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
       'ROTATE_REFRESH_TOKENS': True,
   }

**URLs:**

.. code-block:: python

   from rest_framework_simplejwt.views import (
       TokenObtainPairView,
       TokenRefreshView,
   )

   urlpatterns = [
       path('api/v1/api-token-auth/', TokenObtainPairView.as_view()),
       path('api/v1/api-token-refresh/', TokenRefreshView.as_view()),
   ]

Obtaining Tokens
----------------

**Request:**

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/api-token-auth/ \\
     -H "Content-Type: application/json" \\
     -d '{"email":"user@example.com","password":"password"}'

**Response:**

.. code-block:: json

   {
     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
   }

Using Tokens
------------

.. code-block:: bash

   curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLC..." \\
     http://localhost:8000/api/v1/contracts/

Refreshing Tokens
-----------------

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/api-token-refresh/ \\
     -H "Content-Type: application/json" \\
     -d '{"refresh":"eyJ0eXAiOiJKV1QiLC..."}'

Password Management
===================

Password Hashing
----------------

**Argon2 (recommended):**

.. code-block:: python

   PASSWORD_HASHERS = [
       'django.contrib.auth.hashers.Argon2PasswordHasher',
       'django.contrib.auth.hashers.PBKDF2PasswordHasher',
   ]

**Requires:**

.. code-block:: bash

   pip install argon2-cffi

Password Reset
--------------

**URL:**

.. code-block:: text

   /accounts/password/reset/

**Email template:**

Create ``templates/account/email/password_reset_key_message.txt``

**Flow:**

1. User requests reset → email sent
2. Click link → enter new password
3. Password updated → can log in

Change Password
---------------

.. code-block:: python

   from django.contrib.auth.views import PasswordChangeView

   path('accounts/password/change/', PasswordChangeView.as_view())

Permissions & Authorization
============================

Login Required
--------------

.. code-block:: python

   from django.contrib.auth.decorators import login_required

   @login_required
   def dashboard(request):
       return render(request, 'dashboard.html')

**Class-based views:**

.. code-block:: python

   from django.contrib.auth.mixins import LoginRequiredMixin

   class DashboardView(LoginRequiredMixin, TemplateView):
       template_name = 'dashboard.html'

Permission Level Check
----------------------

.. code-block:: python

   def director_required(function):
       def wrap(request, *args, **kwargs):
           if request.user.nivel_acceso.nivel >= 3:
               return function(request, *args, **kwargs)
           return HttpResponseForbidden()
       return wrap

   @login_required
   @director_required
   def sensitive_view(request):
       ...

See :doc:`permission-levels` for details.

Security Best Practices
=======================

**1. Use HTTPS in production:**

.. code-block:: python

   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True

**2. Strong password requirements:**

.. code-block:: python

   AUTH_PASSWORD_VALIDATORS = [
       {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
       {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
       {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
       {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
   ]

**3. Rate limiting:**

Use django-ratelimit or similar.

**4. Two-factor authentication (optional):**

Use django-otp or django-allauth 2FA.

**5. Session security:**

.. code-block:: python

   SESSION_COOKIE_HTTPONLY = True
   SESSION_COOKIE_SAMESITE = 'Strict'

Troubleshooting
===============

**"User matching query does not exist":**

- Check email is correct
- Verify user exists in database
- Confirm AUTH_USER_MODEL setting

**"Invalid credentials":**

- Verify password is correct
- Check authentication backend is configured
- Ensure user is active (``is_active=True``)

**API 401 Unauthorized:**

- Check token is included in header
- Verify token hasn't expired
- Confirm token format: ``Bearer <token>``

**Session not persisting:**

- Check SESSION_COOKIE_SECURE with HTTP (should be False for local)
- Verify browser accepts cookies
- Check session backend is configured

See Also
========

- :doc:`multi-tenancy` - Multi-company architecture
- :doc:`permission-levels` - Permission system
- :doc:`../api/authentication` - API auth details
- :doc:`../models/users` - User model reference
