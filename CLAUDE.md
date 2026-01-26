# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Construbot is a Django-based operational solution for construction companies (Una Solucion operativa para constructoras). The project is licensed under AGPLv3 and can be deployed as a standalone application or used as a library.

**Current Version:** 1.1.04
**Django Version:** 5.2.10 LTS
**Python Version:** >=3.10 (recommended 3.13.11)
**PostgreSQL Version:** >=14 (recommended 16+)

## Development Commands

### Docker-based Development (Primary Method)

The project uses Docker with separate environments for development, production, and testing. All commands modify the `.env` file to set appropriate environment variables.

**Start development environment:**
```bash
make dev  # Starts redis, postgres, mailhog, and runs django with service ports
```

**Build and start development environment:**
```bash
make buildev  # Builds and starts with local settings and DEBUG=True
```

**Run the Django shell:**
```bash
make shell
```

**Database migrations:**
```bash
make migrations  # Creates and applies migrations
```

**Create superuser:**
```bash
make superuser
```

**Populate database with test data:**
```bash
make poblar  # Runs the custom 'poblar' management command
```

**Stop development environment:**
```bash
make down
```

**Production build:**
```bash
make buildprod  # Builds with production settings and DEBUG=False
```

### Testing

**Run full test suite with coverage:**
```bash
make test  # Runs tests with coverage report
```

**Run tests with warnings enabled:**
```bash
make warningtest
```

**Run only tests tagged as 'current':**
```bash
make current
```

**Local testing (without Docker):**
```bash
make localtest
```

### Docker Cleanup

**Remove all containers:**
```bash
make clean
```

**Remove database containers and volumes:**
```bash
make cleandb
```

**Remove all Docker images and volumes:**
```bash
make cleanhard
```

### Local Development (Without Docker)

**Run development server:**
```bash
make runserver  # Sets USE_DOCKER=no and runs python manage.py runserver
```

### Requirements Management

**Sync local requirements:**
```bash
make mkenv  # Uses pip-sync to install requirements/local.txt
```

**Compile requirements files:**
```bash
make pipcompile  # Compiles base.txt, local.txt, and test.txt from .in files
```

## Architecture

### Settings Configuration

The project uses environment-based settings located in `construbot/config/settings/`:
- `base.py` - Shared settings for all environments
- `local.py` - Development settings
- `test.py` - Testing settings
- `production.py` - Production settings

Settings are controlled via the `DJANGO_SETTINGS_MODULE` environment variable, which is managed by the Makefile targets.

### Environment Variables

The project uses `django-environ` to manage configuration. Environment variables are loaded from the `.env` file when `DJANGO_READ_DOT_ENV_FILE=True`.

Key environment variables:
- `DJANGO_SETTINGS_MODULE` - Controls which settings file is used
- `DJANGO_DEBUG` - Enables/disables debug mode
- `USE_DOCKER` - Determines if running in Docker
- `CONSTRUBOT_AS_LIBRARY` - When True, disables standalone features (admin, accounts)
- `DATABASE_URL` - PostgreSQL connection string

### Application Structure

**Main Django Apps:**
- `construbot.users` - Custom user model and authentication (AUTH_USER_MODEL = 'users.User')
- `construbot.proyectos` - Core business logic for construction projects, contracts, and estimates
- `construbot.core` - Shared utilities and core functionality
- `construbot.account_config` - Account configuration and custom login forms
- `construbot.api` - REST API with JWT authentication (djangorestframework + simplejwt)
- `construbot.taskapp` - Celery task configuration

**Key Third-party Apps:**
- `django-allauth` 65.14.0 - User registration and authentication (v65+ uses new settings format)
- `django-autocomplete-light` (dal) - Autocomplete widgets (must be loaded before admin)
- `django-treebeard` - Tree structures for hierarchical data
- `django-bootstrap4` - Bootstrap 4 integration
- `rest_framework` 3.16.1 - Django REST Framework

### URL Structure

Main URL patterns (from `construbot/config/urls.py`):
- `/` - Redirects to user dashboard (UserRedirectView)
- `/accounts/` - User account management (allauth)
- `/admin/` - Django admin interface
- `/proyectos/` - Project management views
- `/users/` - User management
- `/api/v1/` - REST API endpoints
- `/core/` - Core utilities

When `CONSTRUBOT_AS_LIBRARY=True`, standalone URLs (admin, accounts) are disabled.

### Authentication

The project uses a custom authentication backend at `construbot.core.backends.ModelBackend` and includes:
- JWT authentication for API (rest_framework_simplejwt)
- Session-based authentication for web interface
- Custom user model with company relationships
- Permission levels defined in `NIVELES_ACCESO` (Auxiliar, Coordinador, Director, Corporativo, Soporte, Superusuario)

### Database

- **Primary Database:** PostgreSQL 14+ (recommended 16+)
- **Database Adapter:** psycopg3 (psycopg[binary])
- **Connection:** Managed via `DATABASE_URL` environment variable
- **Atomic Requests:** Enabled by default (`ATOMIC_REQUESTS = True`)
- **Note:** Django 5.2+ requires PostgreSQL 14 or later

### Task Queue

- **Broker:** Redis (redis://redis:6379/0)
- **Worker:** Celery 5.4.0
- **Result Backend:** Redis
- **Serialization:** JSON
- **Time Limits:** Task limit 5 minutes, soft limit 60 seconds

### Static Files and Media

- **Static Root:** `staticfiles/` directory
- **Static URL:** `/static/`
- **Media Root:** `construbot/media/`
- **Media URL:** `/media/`
- **Static Compression:** django-compressor enabled

In production, use WhiteNoise for static file serving and django-storages with S3 for media files.

### Domain Models

The `proyectos` app contains the core business models:
- `Contraparte` - Business relationships (Cliente, Destajista, Subcontratista)
- `Sitio` - Construction sites linked to clients
- `Destinatario` - Recipients for documents
- `Units` - Measurement units
- `Company` - User companies (from users app)

All models are scoped to a `Company` for multi-tenancy support.

### API

REST API uses:
- JWT token authentication (`/api/v1/api-token-auth/`, `/api/v1/api-token-refresh/`)
- Default permission: IsAuthenticated
- Includes data migration endpoints for importing legacy data

## Testing

Tests are located in `tests/` subdirectories within each app. The project uses:
- Django's built-in test framework
- Coverage.py with django_coverage_plugin
- Coverage configuration in `.coveragerc`
- Migrations are disabled during testing for speed (see `manage.py`)

**Running specific test tags:**
Use the `--tag=current` flag or the `make current` command to run only tests marked with the `@tag('current')` decorator.

## Important Notes

1. **AutoComplete Light:** The `dal` and `dal_select2` apps must be in `INSTALLED_APPS` before `django.contrib.admin`

2. **Library Mode:** When `CONSTRUBOT_AS_LIBRARY=True`, the application runs as a library without standalone features like admin and account management

3. **Localization:** The application is configured for Spanish (Mexico) with timezone `America/Mexico_City`

4. **Email Backend:** Configured via `DJANGO_EMAIL_BACKEND`, uses django-anymail for various providers (Mailgun, Postmark, SendGrid)

5. **Password Hashing:** Uses Argon2 as the primary password hasher

6. **Sentry Integration:** Sentry SDK is installed for error tracking in production

7. **Django 5.2 Upgrade Notes:**
   - Requires PostgreSQL 14 or later (Docker uses PostgreSQL 16)
   - Uses psycopg3 instead of psycopg2-binary
   - django-allauth upgraded from 0.63.6 to 65.14.0 with new settings format
   - Test API changes: `assertQuerysetEqual` → `assertQuerySetEqual`, `assertFormError`/`assertFormsetError` now require form object instead of response
   - Python 3.13 support requires cffi 2.0+ and argon2-cffi 25.1+

8. **Docker Configuration:**
   - Python 3.13.1-alpine3.21
   - PostgreSQL 16-alpine
   - Redis 7-alpine
   - pip-tools 7.5.2
