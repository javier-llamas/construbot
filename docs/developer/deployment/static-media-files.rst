====================
Static & Media Files
====================

Configuration for serving static files and user-uploaded media in production.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

Construbot handles two types of files:

1. **Static files** - CSS, JavaScript, images (part of application code)
2. **Media files** - User uploads (PDFs, images, documents)

In production, these should be served differently than in development for performance and scalability.

Static Files Strategy
======================

WhiteNoise (Recommended for Small Deployments)
-----------------------------------------------

**What is WhiteNoise:**

- Serves static files directly from Django
- No separate web server configuration needed
- Gzip compression built-in
- CDN-friendly with far-future cache headers

**Already configured** in ``construbot.config.settings.production``:

.. code-block:: python

   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',  # After Security, before others
       ...
   ]

   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

**Collect static files:**

.. code-block:: bash

   docker compose run --rm django python manage.py collectstatic --no-input

**Verify:**

.. code-block:: bash

   ls staticfiles/
   # Should contain: admin/, css/, js/, staticfiles.json

**Benefits:**

- Simple setup
- No CDN required
- Efficient for <10,000 users
- Compression and caching built-in

CDN (CloudFront/CloudFlare)
----------------------------

For higher traffic, serve static files through a CDN:

**AWS CloudFront setup:**

.. code-block:: bash

   # Create S3 bucket for static files
   aws s3 mb s3://construbot-static-yourdomain

   # Sync static files to S3
   aws s3 sync staticfiles/ s3://construbot-static-yourdomain/static/

   # Create CloudFront distribution
   aws cloudfront create-distribution \\
     --origin-domain-name construbot-static-yourdomain.s3.amazonaws.com \\
     --default-root-object index.html

**Update settings:**

.. code-block:: bash

   # In .env
   STATIC_URL=https://d111111abcdef8.cloudfront.net/static/

**Benefits:**

- Global distribution
- Lower latency
- Offload traffic from application servers
- Reduced bandwidth costs

Media Files Strategy
====================

Amazon S3 (Recommended)
-----------------------

**Why S3:**

- Unlimited scalable storage
- High availability (99.99%)
- Integrated with Django via django-storages
- Can use CloudFront CDN
- Automatic backups with versioning

**Setup S3 bucket:**

.. code-block:: bash

   # Create bucket
   aws s3 mb s3://construbot-media-yourdomain --region us-east-1

   # Block public access (recommended - use signed URLs)
   aws s3api put-public-access-block \\
     --bucket construbot-media-yourdomain \\
     --public-access-block-configuration \\
       "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

   # Enable versioning (optional, for backups)
   aws s3api put-bucket-versioning \\
     --bucket construbot-media-yourdomain \\
     --versioning-configuration Status=Enabled

   # Configure CORS (if accessing from different domain)
   aws s3api put-bucket-cors \\
     --bucket construbot-media-yourdomain \\
     --cors-configuration file://cors.json

**cors.json:**

.. code-block:: json

   {
     "CORSRules": [
       {
         "AllowedOrigins": ["https://yourdomain.com"],
         "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
         "AllowedHeaders": ["*"],
         "MaxAgeSeconds": 3000
       }
     ]
   }

**Create IAM user:**

.. code-block:: bash

   # Create user
   aws iam create-user --user-name construbot-s3

   # Create policy
   cat > s3-policy.json <<EOF
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": ["s3:*"],
         "Resource": [
           "arn:aws:s3:::construbot-media-yourdomain",
           "arn:aws:s3:::construbot-media-yourdomain/*"
         ]
       }
     ]
   }
   EOF

   # Attach policy
   aws iam put-user-policy \\
     --user-name construbot-s3 \\
     --policy-name S3FullAccess \\
     --policy-document file://s3-policy.json

   # Create access keys
   aws iam create-access-key --user-name construbot-s3

**Configure Django:**

.. code-block:: bash

   # In .env
   USE_S3=True
   AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
   AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   AWS_STORAGE_BUCKET_NAME=construbot-media-yourdomain
   AWS_S3_REGION_NAME=us-east-1

   # Optional: Custom domain (CloudFront)
   AWS_S3_CUSTOM_DOMAIN=d111111abcdef8.cloudfront.net

**Already configured** in ``construbot.config.settings.production``:

.. code-block:: python

   if env.bool('USE_S3', default=False):
       AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
       AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
       AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
       AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')

       # Media files
       DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

       # Optional: CloudFront
       if env('AWS_S3_CUSTOM_DOMAIN', default=None):
           AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')

**Test upload:**

.. code-block:: bash

   # Django shell
   docker compose run --rm django python manage.py shell

.. code-block:: python

   from django.core.files.base import ContentFile
   from django.core.files.storage import default_storage

   # Upload test file
   path = default_storage.save('test.txt', ContentFile(b'Hello S3'))
   print(f"File saved to: {path}")

   # Verify in S3
   # aws s3 ls s3://construbot-media-yourdomain/

DigitalOcean Spaces
-------------------

**Alternative to S3:**

.. code-block:: bash

   # In .env
   USE_S3=True  # Spaces uses S3-compatible API
   AWS_ACCESS_KEY_ID=your-spaces-key
   AWS_SECRET_ACCESS_KEY=your-spaces-secret
   AWS_STORAGE_BUCKET_NAME=construbot-media
   AWS_S3_ENDPOINT_URL=https://nyc3.digitaloceanspaces.com
   AWS_S3_REGION_NAME=nyc3

**Cheaper than S3** for high bandwidth usage.

Local Storage (Small Deployments)
----------------------------------

For small deployments without cloud storage:

.. code-block:: bash

   # In .env
   USE_S3=False

**Configure Nginx** to serve media files:

.. code-block:: nginx

   location /media/ {
       alias /app/media/;
       expires 1y;
       add_header Cache-Control "public";
   }

**Mount media volume** in docker-compose.yml:

.. code-block:: yaml

   django:
     volumes:
       - media_volume:/app/media

   nginx:
     volumes:
       - media_volume:/app/media:ro

**Backup strategy required** - rsync to remote server or S3.

Static Files Configuration
===========================

Settings Reference
------------------

**base.py:**

.. code-block:: python

   # Static files (CSS, JavaScript, Images)
   STATIC_ROOT = str(ROOT_DIR / 'staticfiles')
   STATIC_URL = '/static/'
   STATICFILES_DIRS = [
       str(APPS_DIR / 'static'),
   ]

**production.py:**

.. code-block:: python

   # WhiteNoise
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

   # Or with CDN:
   STATIC_URL = 'https://cdn.yourdomain.com/static/'

Collecting Static Files
------------------------

**During deployment:**

.. code-block:: bash

   docker compose run --rm django python manage.py collectstatic --no-input

**What happens:**

1. Gathers all static files from apps and STATICFILES_DIRS
2. Processes them (minification, hashing)
3. Copies to STATIC_ROOT (``staticfiles/``)
4. Creates ``staticfiles.json`` manifest

**Manifest system:**

.. code-block:: json

   {
     "version": "1.0",
     "paths": {
       "css/main.css": "css/main.abc123.css",
       "js/app.js": "js/app.def456.js"
     }
   }

**Benefits:**

- Cache busting (unique filenames)
- Far-future cache headers
- Automatic compression (gzip/brotli)

Custom Static Files
-------------------

**Add custom CSS/JS:**

.. code-block:: bash

   # Place in
   construbot/static/css/custom.css
   construbot/static/js/custom.js

**In templates:**

.. code-block:: html+django

   {% load static %}
   <link rel="stylesheet" href="{% static 'css/custom.css' %}">
   <script src="{% static 'js/custom.js' %}"></script>

**Recollect after changes:**

.. code-block:: bash

   docker compose run --rm django python manage.py collectstatic --no-input

Media Files Configuration
==========================

Settings Reference
------------------

**base.py:**

.. code-block:: python

   # Media files (user uploads)
   MEDIA_ROOT = str(APPS_DIR / 'media')
   MEDIA_URL = '/media/'

**production.py with S3:**

.. code-block:: python

   if USE_S3:
       DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
       MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/' if AWS_S3_CUSTOM_DOMAIN \\
                   else f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'

File Upload Handling
--------------------

**In models (example):**

.. code-block:: python

   from django.db import models

   class Document(models.Model):
       file = models.FileField(upload_to='documents/%Y/%m/%d/')
       uploaded_at = models.DateTimeField(auto_now_add=True)

**Upload to S3:**

.. code-block:: python

   # In views or forms
   document = Document.objects.create(file=request.FILES['file'])
   # File automatically uploaded to S3

**File URL:**

.. code-block:: python

   # Get file URL
   url = document.file.url
   # Returns: https://bucket.s3.amazonaws.com/documents/2024/01/15/file.pdf

Signed URLs (Private Files)
----------------------------

**For secure file access:**

.. code-block:: python

   from django.core.files.storage import default_storage

   # Generate signed URL (expires in 1 hour)
   url = default_storage.url('path/to/file.pdf', expire=3600)

**Configure S3 settings:**

.. code-block:: python

   # In production.py
   AWS_QUERYSTRING_AUTH = True  # Use signed URLs
   AWS_S3_FILE_OVERWRITE = False  # Don't overwrite files
   AWS_DEFAULT_ACL = None  # Use bucket ACL

Optimization
============

Image Optimization
------------------

**Install Pillow (already included):**

.. code-block:: python

   from PIL import Image
   from io import BytesIO
   from django.core.files.base import ContentFile

   def optimize_image(image_field):
       img = Image.open(image_field)

       # Resize if too large
       if img.width > 1920:
           img.thumbnail((1920, 1920), Image.LANCZOS)

       # Convert to RGB if needed
       if img.mode != 'RGB':
           img = img.convert('RGB')

       # Save with optimization
       output = BytesIO()
       img.save(output, format='JPEG', quality=85, optimize=True)
       output.seek(0)

       return ContentFile(output.read())

Compression
-----------

**Static files** (WhiteNoise handles automatically):

- Gzip compression
- Brotli compression (if installed)

**Manual compression:**

.. code-block:: bash

   # Install brotli
   pip install brotli

   # In production.py
   WHITENOISE_COMPRESSION = True  # Default

Caching
-------

**Static files caching:**

.. code-block:: nginx

   location /static/ {
       alias /app/staticfiles/;
       expires 1y;
       add_header Cache-Control "public, immutable";
   }

**Media files caching:**

.. code-block:: nginx

   location /media/ {
       alias /app/media/;
       expires 30d;
       add_header Cache-Control "public";
   }

CDN Setup
=========

CloudFront for S3
-----------------

**Create distribution:**

.. code-block:: bash

   aws cloudfront create-distribution \\
     --origin-domain-name construbot-media-yourdomain.s3.amazonaws.com \\
     --comment "Construbot media files" \\
     --default-cache-behavior '{
       "TargetOriginId": "S3-construbot-media",
       "ViewerProtocolPolicy": "redirect-to-https",
       "AllowedMethods": {"Items": ["GET", "HEAD"], "Quantity": 2},
       "CachedMethods": {"Items": ["GET", "HEAD"], "Quantity": 2},
       "ForwardedValues": {
         "QueryString": false,
         "Cookies": {"Forward": "none"}
       },
       "MinTTL": 0,
       "DefaultTTL": 86400,
       "MaxTTL": 31536000
     }'

**Update Django settings:**

.. code-block:: bash

   # In .env
   AWS_S3_CUSTOM_DOMAIN=d111111abcdef8.cloudfront.net

CloudFlare
----------

**Setup:**

1. Add domain to CloudFlare
2. Update nameservers
3. Enable caching for static/media paths
4. Configure page rules

**Page rule for static files:**

.. code-block:: text

   URL: *yourdomain.com/static/*
   Cache Level: Cache Everything
   Edge Cache TTL: 1 year

Backup and Recovery
===================

S3 Versioning
-------------

.. code-block:: bash

   # Enable versioning
   aws s3api put-bucket-versioning \\
     --bucket construbot-media-yourdomain \\
     --versioning-configuration Status=Enabled

   # List versions
   aws s3api list-object-versions --bucket construbot-media-yourdomain

   # Restore previous version
   aws s3api copy-object \\
     --copy-source construbot-media-yourdomain/path/to/file.pdf?versionId=xxx \\
     --bucket construbot-media-yourdomain \\
     --key path/to/file.pdf

S3 Lifecycle Policies
----------------------

**Delete old files automatically:**

.. code-block:: json

   {
     "Rules": [
       {
         "Id": "DeleteOldVersions",
         "Status": "Enabled",
         "NoncurrentVersionExpiration": {
           "NoncurrentDays": 90
         }
       },
       {
         "Id": "TransitionToGlacier",
         "Status": "Enabled",
         "Transitions": [
           {
             "Days": 365,
             "StorageClass": "GLACIER"
           }
         ]
       }
     ]
   }

.. code-block:: bash

   aws s3api put-bucket-lifecycle-configuration \\
     --bucket construbot-media-yourdomain \\
     --lifecycle-configuration file://lifecycle.json

Local Backup
------------

**Sync S3 to local:**

.. code-block:: bash

   # Backup media files locally
   aws s3 sync s3://construbot-media-yourdomain /backup/media/

   # Schedule with cron
   0 3 * * * aws s3 sync s3://construbot-media-yourdomain /backup/media/

Troubleshooting
===============

Static Files Not Loading
-------------------------

.. code-block:: bash

   # Recollect
   docker compose run --rm django python manage.py collectstatic --clear --no-input

   # Check STATIC_ROOT
   ls -la staticfiles/

   # Verify STATIC_URL in settings
   docker compose run --rm django python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.STATIC_URL)

File Upload Failing
-------------------

**Check S3 permissions:**

.. code-block:: bash

   # Test AWS credentials
   aws s3 ls s3://construbot-media-yourdomain

   # Check Django settings
   docker compose run --rm django python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.DEFAULT_FILE_STORAGE)
   >>> print(settings.AWS_STORAGE_BUCKET_NAME)

**Test upload:**

.. code-block:: python

   from django.core.files.base import ContentFile
   from django.core.files.storage import default_storage
   path = default_storage.save('test.txt', ContentFile(b'test'))
   print(path)

CORS Errors
-----------

**Update S3 CORS:**

.. code-block:: bash

   aws s3api put-bucket-cors \\
     --bucket construbot-media-yourdomain \\
     --cors-configuration file://cors.json

**Allow your domain** in cors.json AllowedOrigins.

See Also
========

- :doc:`production-checklist` - Deployment checklist
- :doc:`aws-ec2` - AWS deployment guide
- :doc:`environment-variables` - Environment configuration
- `django-storages documentation <https://django-storages.readthedocs.io/>`_
- `WhiteNoise documentation <http://whitenoise.evans.io/>`_
