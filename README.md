# Construbot

> **An operational solution for construction companies**
> Modern Django-based construction management platform

[![Documentation Status](https://readthedocs.org/projects/construbot/badge/?version=latest)](https://construbot.readthedocs.io/en/latest/?badge=latest)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-3.2.25-green)](https://www.djangoproject.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🏗️ What is Construbot?

**Construbot** is a comprehensive, open-source construction management system built with Django. It provides construction companies with the tools they need to manage projects, track finances, handle contracts, and generate estimates—all in one integrated platform.

### Key Features

- 📋 **Contract Management** - Complete lifecycle management with hierarchical support
- 💰 **Financial Tracking** - Estimates, retentions, progress payments
- 🏢 **Multi-Tenancy** - Support for multiple companies in a single deployment
- 📊 **Progress Billing** - Automated estimate generation and tracking
- 🔐 **Role-Based Access** - Six-tier permission system
- 📄 **Document Generation** - PDF invoices, estimates, and reports
- 📦 **Excel Integration** - Bulk import of catalogs and concepts
- 🌳 **Hierarchical Contracts** - Parent-child relationships for subcontracts
- 🌍 **Bilingual Support** - Spanish/English interface

## 🎯 Why Construbot?

### The Problem

Construction companies face unique operational challenges:

- **Complex billing structures** with retentions, advance payments, and progress billing
- **Multiple subcontractors** requiring separate tracking and coordination
- **Detailed project catalogs** with hundreds of line items and units of measurement
- **Compliance requirements** for documentation and financial tracking
- **Manual processes** leading to errors and inefficiencies

### The Solution

Construbot addresses these challenges by providing:

✅ **Centralized project management** with all contracts, sites, and contacts in one place

✅ **Automated financial calculations** for estimates, retentions, and cumulative tracking

✅ **Professional document generation** with standardized templates

✅ **Audit trails** with complete history of changes and approvals

✅ **Flexible architecture** that adapts to your workflow

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12+ (recommended) or SQLite for development
- Redis (for Celery tasks)
- Docker & Docker Compose (recommended for quick setup)

### Installation

#### Option 1: Docker (Recommended)

The fastest way to get started:

```bash
# Clone the repository
git clone https://github.com/javier-llamas/construbot.git
cd construbot

# Build and start the development environment
make buildev

# Create a superuser
make superuser

# (Optional) Populate with test data
make poblar
```

Access the application at **http://localhost:8000**

#### Option 2: Local Development

For local development without Docker:

```bash
# Clone the repository
git clone https://github.com/javier-llamas/construbot.git
cd construbot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/local.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Access the application at **http://localhost:8000**

### First Steps

1. **Log in** with your superuser credentials
2. **Create a company** for your organization
3. **Add counterparties** (clients, subcontractors)
4. **Create a site** for your first project
5. **Set up a contract** with concepts and retentions
6. **Generate your first estimate** for progress billing

## 📚 Documentation

Comprehensive documentation is available at **[construbot.readthedocs.io](https://construbot.readthedocs.io/)**

### Documentation Sections

- 📖 **[User Guide](https://construbot.readthedocs.io/en/latest/user-guide/)** - For end users and project managers
  - Concepts: Projects, Contracts, Estimates, Counterparties
  - Workflows: Creating projects, managing estimates, generating reports
  - Features: Hierarchical contracts, Excel import, PDF generation

- 🔧 **[Developer Guide](https://construbot.readthedocs.io/en/latest/developer/)** - For developers and system administrators
  - Installation: Docker setup, local development, production deployment
  - Architecture: Multi-tenancy, authentication, database schema
  - API: REST API documentation and examples

- 🤝 **[Contributor Guide](https://construbot.readthedocs.io/en/latest/contributor/)** - For open-source contributors
  - Getting started with development
  - Code style and testing guidelines
  - Translation and documentation contributions

### Quick Links

- [Installation Guide](https://construbot.readthedocs.io/en/latest/developer/installation/)
- [Docker Setup](https://construbot.readthedocs.io/en/latest/developer/installation/docker-setup/)
- [API Reference](https://construbot.readthedocs.io/en/latest/developer/api/)
- [Makefile Commands](https://construbot.readthedocs.io/en/latest/reference/makefile-commands/)

## 🛠️ Technology Stack

- **Backend:** Django 3.2.19, Django REST Framework
- **Database:** PostgreSQL with django-treebeard for hierarchical data
- **Task Queue:** Celery with Redis
- **Authentication:** JWT (SimpleJWT) + Session-based
- **Frontend:** Django templates with Bootstrap 4
- **API:** RESTful API with JWT authentication
- **Deployment:** Docker, Docker Compose, WhiteNoise for static files

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, improving documentation, or translating to new languages, your help is appreciated.

### How to Contribute

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/construbot.git
   cd construbot
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** following our code style guidelines
5. **Test your changes**:
   ```bash
   make test
   ```
6. **Commit and push** your changes:
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request** on GitHub

### Contribution Guidelines

- **Code Style:** Follow PEP 8, use `black` for formatting, `isort` for imports
- **Testing:** Write tests for new features, maintain coverage above 80%
- **Documentation:** Update docs for any user-facing changes
- **Commit Messages:** Use clear, descriptive commit messages
- **Pull Requests:** Reference related issues, provide context

See our [Contributor Guide](https://construbot.readthedocs.io/en/latest/contributor/) for detailed guidelines.

### Development Setup

```bash
# Set up development environment
make buildev

# Run tests with coverage
make test

# Run tests with warnings
make warningtest

# Run linting
flake8 construbot/

# Format code
black .
isort .
```

## 📋 Project Structure

```
construbot/
├── construbot/              # Main Django project
│   ├── users/              # Custom user model and authentication
│   ├── proyectos/          # Core business logic (contracts, estimates)
│   ├── core/               # Shared utilities
│   ├── api/                # REST API endpoints
│   ├── account_config/     # Account configuration
│   └── config/             # Django settings
├── docs/                   # Sphinx documentation
├── requirements/           # Python dependencies
├── tests/                  # Test suite
├── Makefile               # Development commands
└── docker-compose.yml     # Docker configuration
```

## 🌍 Internationalization

Construbot supports both Spanish and English:

- **Primary Language:** Spanish (codebase and models use Spanish terminology)
- **Secondary Language:** English (documentation and UI translations available)
- **Translation Support:** Built-in with django-rosetta for easy translation management

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

This means:
- ✅ You can use, modify, and distribute this software
- ✅ You must disclose the source code when distributing
- ✅ Network use counts as distribution (SaaS clause)
- ✅ Modifications must also be AGPL-licensed

See [LICENSE](LICENSE) for full details.

## 🙏 Acknowledgments

- Built with [Django](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/)
- Tree structures powered by [django-treebeard](https://django-treebeard.readthedocs.io/)
- Documentation built with [Sphinx](https://www.sphinx-doc.org/) and hosted on [ReadTheDocs](https://readthedocs.org/)
- UI built with [Bootstrap 4](https://getbootstrap.com/)

## 📞 Support & Community

- **Documentation:** [construbot.readthedocs.io](https://construbot.readthedocs.io/)
- **Issues:** [GitHub Issues](https://github.com/javier-llamas/construbot/issues)
- **Discussions:** [GitHub Discussions](https://github.com/javier-llamas/construbot/discussions)
- **Email:** [Contact](mailto:javier.llamas@example.com)

## 🗺️ Roadmap

Future enhancements we're considering:

- [ ] Mobile application (iOS/Android)
- [ ] Advanced reporting and analytics dashboard
- [ ] Integration with accounting software (QuickBooks, Xero)
- [ ] Multi-currency support
- [ ] Equipment and resource management
- [ ] Time tracking and labor management
- [ ] Enhanced document management with e-signatures

## ⭐ Show Your Support

If you find Construbot useful, please consider:

- Giving it a ⭐ on GitHub
- Sharing it with others in the construction industry
- Contributing code, documentation, or translations
- Reporting bugs and suggesting features

---

**Made with ❤️ for the construction industry**

*Current Version: 1.1.04*
