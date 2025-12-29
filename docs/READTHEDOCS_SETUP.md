# ReadTheDocs Setup Guide

Complete guide for deploying Construbot documentation on ReadTheDocs.

## Prerequisites

- GitHub repository with documentation: https://github.com/javier-llamas/construbot
- ReadTheDocs account (free): https://readthedocs.org
- Admin access to the GitHub repository

## Quick Start

### 1. Verify Local Build

Before deploying to ReadTheDocs, ensure documentation builds locally:

```bash
cd docs
pip install -r requirements.txt
make clean
make html
```

**Expected output:** HTML documentation generated in `_build/html/`

**Test both languages:**

```bash
make html-en  # English version
make html-es  # Spanish version (requires translations)
```

Open `_build/html/index.html` in your browser to verify.

### 2. Connect to ReadTheDocs

#### Step 2.1: Create Account

1. Go to https://readthedocs.org
2. Sign up using GitHub account (recommended)
3. Authorize ReadTheDocs to access your repositories

#### Step 2.2: Import Project

1. Click **"Import a Project"** from dashboard
2. Select **"Import Manually"**
3. Fill in project details:
   - **Name:** `construbot`
   - **Repository URL:** `https://github.com/javier-llamas/construbot`
   - **Repository type:** Git
   - **Default branch:** `master`
4. Click **"Next"**

#### Step 2.3: Configure Build

ReadTheDocs will auto-detect `.readthedocs.yaml` configuration.

**Verify settings:**

- **Programming Language:** Python
- **Python version:** 3.9
- **Configuration file:** `.readthedocs.yaml` (detected)

Click **"Finish"**

### 3. Trigger First Build

ReadTheDocs automatically triggers the first build.

**Monitor build progress:**

1. Go to **"Builds"** tab
2. Click on latest build
3. View build logs

**Expected build time:** 5-10 minutes

### 4. Verify Deployment

Once build completes:

1. Click **"View Docs"**
2. Default URL: `https://construbot.readthedocs.io/en/latest/`

**Test navigation:**

- ✓ Main index page loads
- ✓ User Guide section accessible
- ✓ Developer section accessible
- ✓ Contributor section accessible
- ✓ Search functionality works

### 5. Configure Language Versions

ReadTheDocs supports multiple language versions:

1. Go to **Admin → Translations**
2. Add Spanish version if not auto-detected
3. Set English as primary language

**Access URLs:**

- English: `https://construbot.readthedocs.io/en/latest/`
- Spanish: `https://construbot.readthedocs.io/es/latest/`

## Configuration Files

### .readthedocs.yaml

Located at repository root. Controls build process:

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.9"
  jobs:
    post_build:
      - cd docs && make gettext && sphinx-intl update -p _build/gettext -l es

sphinx:
  configuration: docs/conf.py
  fail_on_warning: false

python:
  install:
    - requirements: docs/requirements.txt
    - method: pip
      path: .
      extra_requirements:
        - docs

formats:
  - pdf
  - epub
  - htmlzip

search:
  ranking:
    'user-guide/*': 2
    'developer/*': 1
    'contributor/*': 0
```

### docs/requirements.txt

All Sphinx dependencies:

```txt
Sphinx==6.2.1
furo==2023.9.10
sphinx-copybutton==0.5.2
sphinxcontrib-httpdomain==1.8.1
sphinx-tabs==3.4.1
sphinx-intl==2.1.0
django==3.2.19
djangorestframework==3.13.1
django-treebeard==4.5.1
django-environ==0.9.0
psycopg2-binary==2.9.6
```

### docs/conf.py

Sphinx configuration with:

- Django setup for autodoc
- Bilingual support (en/es)
- Furo theme (modern, clean design with dark mode)
- Custom extensions

## Webhook Configuration

ReadTheDocs automatically configures a GitHub webhook for automatic builds.

**Verify webhook:**

1. Go to GitHub repo → **Settings → Webhooks**
2. Find ReadTheDocs webhook
3. Verify: ✓ Active, ✓ SSL verification enabled

**Trigger:** Every push to `master` branch triggers rebuild

## Build Troubleshooting

### Common Build Errors

#### Error: "requirements.txt not found"

**Solution:** Verify `docs/requirements.txt` exists in repository

```bash
git add docs/requirements.txt
git commit -m "Add Sphinx build requirements"
git push
```

#### Error: "Django import failed"

**Cause:** Django not configured before autodoc imports

**Solution:** Verify `docs/conf.py` includes Django setup:

```python
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'construbot.config.settings.local'
django.setup()
```

#### Error: "Sphinx build failed with warnings"

**Solution:** Set `fail_on_warning: false` in `.readthedocs.yaml`

Or fix warnings in RST files (check build logs for details)

#### Error: "Spanish translation not found"

**Cause:** Spanish .po files not generated

**Solution:** Run locally and commit:

```bash
cd docs
make gettext
sphinx-intl update -p _build/gettext -l es
git add locale/
git commit -m "Add Spanish translation files"
git push
```

### Viewing Build Logs

1. Go to ReadTheDocs project → **Builds**
2. Click on failed build
3. Expand **"View full log"**
4. Search for error messages

## Advanced Configuration

### Custom Domain

1. Go to **Admin → Domains**
2. Add custom domain: `docs.yourdomain.com`
3. Configure DNS CNAME record:
   - Name: `docs`
   - Value: `construbot.readthedocs.io`
4. Enable HTTPS (automatic with Let's Encrypt)

### Version Management

ReadTheDocs can build multiple versions:

**Activate versions:**

1. Go to **Versions** tab
2. Activate desired versions (tags/branches)
3. Set `latest` as default version

**Version URLs:**

- Latest: `https://construbot.readthedocs.io/en/latest/`
- Stable: `https://construbot.readthedocs.io/en/stable/`
- Specific: `https://construbot.readthedocs.io/en/v1.1.04/`

### PDF/EPUB Downloads

Configured in `.readthedocs.yaml`:

```yaml
formats:
  - pdf
  - epub
  - htmlzip
```

**Download links appear automatically** on documentation pages.

### Search Ranking

Boost important sections in search (values must be integers from -10 to 10):

```yaml
search:
  ranking:
    'user-guide/*': 2      # User docs ranked highest
    'developer/*': 1       # Developer docs normal ranking
    'contributor/*': 0     # Contributor docs lower ranking
```

## Maintenance

### Updating Documentation

**Workflow:**

1. Make changes to RST files locally
2. Test build: `make html`
3. Commit and push to GitHub
4. ReadTheDocs auto-rebuilds (2-5 minutes)
5. Verify changes at readthedocs.io

### Updating Translations

**Spanish translation workflow:**

1. Update English RST files
2. Extract translatable strings:
   ```bash
   cd docs
   make gettext
   ```
3. Update Spanish .po files:
   ```bash
   sphinx-intl update -p _build/gettext -l es
   ```
4. Edit .po files in `docs/locale/es/LC_MESSAGES/`
5. Test Spanish build:
   ```bash
   make html-es
   ```
6. Commit .po files and push

### Monitoring Builds

**Setup notifications:**

1. Go to **Admin → Notifications**
2. Add email for build failures
3. Configure webhook notifications (optional)

**Build badges:**

Add to README.md:

```markdown
[![Documentation Status](https://readthedocs.org/projects/construbot/badge/?version=latest)](https://construbot.readthedocs.io/en/latest/?badge=latest)
```

## Verification Checklist

After deployment, verify:

- [ ] English documentation builds without errors
- [ ] Spanish documentation builds (even if not fully translated)
- [ ] All main sections accessible (User Guide, Developer, Contributor)
- [ ] Search functionality works
- [ ] PDF download available
- [ ] EPUB download available
- [ ] Navigation menu complete
- [ ] Cross-references work (`:doc:` links)
- [ ] Code blocks render properly
- [ ] Tables display correctly
- [ ] Screenshots placeholders visible (invisible comments work)
- [ ] GitHub "Edit on GitHub" links work

## Next Steps

1. **Add Screenshots:** Replace invisible screenshot comments with actual images
2. **Complete Spanish Translation:** Translate .po files for user-facing content
3. **Custom Domain:** Configure docs.construbot.com (optional)
4. **Version Tags:** Create git tags for versioned documentation
5. **Analytics:** Add Google Analytics (Admin → Integrations)

## Support Resources

- **ReadTheDocs Documentation:** https://docs.readthedocs.io/
- **Sphinx Documentation:** https://www.sphinx-doc.org/
- **sphinx-intl Guide:** https://sphinx-intl.readthedocs.io/
- **Community Support:** https://readthedocs.org/support/

## Quick Reference

**Build Documentation Locally:**

```bash
cd docs
make html           # English only
make html-es        # Spanish only
make html-all       # Both languages
make livehtml       # Auto-rebuild server
```

**Update Translations:**

```bash
cd docs
make gettext                              # Extract strings
make update-translations                  # Update .po files
# Edit locale/es/LC_MESSAGES/*.po
make html-es                              # Test Spanish build
```

**Force ReadTheDocs Rebuild:**

1. Go to **Builds** tab
2. Click **"Build Version: latest"**

**Access Build Logs:**

Project → Builds → [build number] → View full log

---

**Questions?** Check ReadTheDocs build logs or open an issue on GitHub.
