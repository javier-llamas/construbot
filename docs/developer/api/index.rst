=======
API
=======

REST API documentation for Construbot.

Overview
========

Construbot provides a REST API built with Django REST Framework for mobile apps and external integrations.

**Base URL:** ``/api/v1/``

**Authentication:** JWT (JSON Web Tokens)

**Format:** JSON

Quick Start
===========

**1. Obtain Token:**

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/api-token-auth/ \\
     -H "Content-Type: application/json" \\
     -d '{"email":"user@example.com","password":"password"}'

   # Response:
   # {"access": "eyJ0...", "refresh": "eyJ0..."}

**2. Use Token:**

.. code-block:: bash

   curl -H "Authorization: Bearer eyJ0..." \\
     http://localhost:8000/api/v1/contracts/

**3. Refresh Token:**

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/api-token-refresh/ \\
     -d '{"refresh":"eyJ0..."}'

Authentication
==============

**JWT Tokens:**

- Access token lifetime: 1 hour
- Refresh token lifetime: 7 days
- Tokens rotate on refresh

**Header format:**

.. code-block:: text

   Authorization: Bearer <access_token>

**Endpoints:**

- ``POST /api/v1/api-token-auth/`` - Obtain token pair
- ``POST /api/v1/api-token-refresh/`` - Refresh access token
- ``POST /api/v1/api-token-verify/`` - Verify token validity

API Endpoints
=============

**Contracts:**

- ``GET /api/v1/contracts/`` - List contracts
- ``POST /api/v1/contracts/`` - Create contract
- ``GET /api/v1/contracts/:id/`` - Retrieve contract
- ``PUT /api/v1/contracts/:id/`` - Update contract
- ``DELETE /api/v1/contracts/:id/`` - Delete contract

**Estimates:**

- ``GET /api/v1/estimates/`` - List estimates
- ``POST /api/v1/estimates/`` - Create estimate

**Counterparties:**

- ``GET /api/v1/contrapartes/`` - List counterparties
- ``POST /api/v1/contrapartes/`` - Create counterparty

Response Format
===============

**Success (200):**

.. code-block:: json

   {
     "count": 100,
     "next": "http://api.example.com/api/v1/contracts/?page=2",
     "previous": null,
     "results": [
       {
         "id": 1,
         "folio": "C-001",
         "company": 1,
         "contraparte": "Acme Corp",
         "monto": "1000000.00"
       }
     ]
   }

**Error (400):**

.. code-block:: json

   {
     "detail": "Invalid input",
     "errors": {
       "folio": ["This field is required."]
     }
   }

Permissions
===========

**All endpoints require authentication.**

**Company scoping:** Results filtered by user's active_company.

**Permission levels:** See :doc:`../architecture/permission-levels`

See Also
========

- :doc:`../architecture/overview` - Architecture
- :doc:`../models/index` - Data models
- :doc:`../installation/index` - Development setup
