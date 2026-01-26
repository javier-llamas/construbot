import os
import re
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('construbot')

setup(
    name='django-construbot',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='GNU Affero General Public License v3',
    description='Una Solucion operativa para constructoras.',
    long_description=README,
    url='https://www.construbot.com.mx/',
    author='Javier Llamas Ramirez',
    author_email='elyak.123@gmail.com',
    python_requires='>=3.10',
    install_requires=[
        # Django LTS 5.2
        'django[argon2]>=5.2,<5.3',
        # REST - Django REST Framework
        'djangorestframework>=3.16,<4.0',
        'djangorestframework_simplejwt>=5.4,<6.0',
        # Configuration
        'django-environ>=0.11.2',
        'whitenoise>=6.8',
        # Models
        'django-model-utils>=4.5',
        'django-treebeard>=4.7',
        # Images
        'Pillow>=11.0.0',
        # For user registration
        'django-allauth>=65.0,<66.0',
        # Python-PostgreSQL Database Adapter - psycopg3
        'psycopg[binary]>=3.2,<4.0',
        # Unicode slugification
        'awesome-slugify==1.6.5',
        # Time zones support
        'pytz==2024.2',
        # Redis support
        'django-redis==5.4.0',
        'redis==5.2.1',
        # Celery support
        'celery==5.4.0',
        # Compressing static files
        'rcssmin>=1.1.1',
        'django-compressor>=4.6',
        # FrontEnd Libraries
        'django-autocomplete-light==3.11.0',
        'django-bootstrap4==23.4',
        # xls files handling
        'openpyxl==3.1.5',
        # WSGI Handler
        'gunicorn==23.0.0',
        # Static and Media Storage
        'django-storages[boto3]==1.14.4',
        # Email backends for Mailgun, Postmark, SendGrid and more
        'django-anymail>=11.0,<12.0',
        # Sentry client
        'sentry-sdk>=2.19.2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 5.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
