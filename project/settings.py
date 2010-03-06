# Django settings for project project.

import os
import socket

hostname = socket.gethostname()

try:
    environ = {
        'refugeebuddy.org': 'production'
    }[hostname]
except KeyError:
    environ = 'development'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG

ADMINS = (
    ('Ozan Onay', 'ozan@digitaleskimo.net'),
)

MANAGERS = ADMINS

if environ == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.path.join(PROJECT_ROOT, '../dev.db'),                      # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
elif environ == 'production':
    DATABASES = {
       'default': {
           'ENGINE': 'postgresql_psycopg2', #'postgresql', 'mysql', 'sqlite3' or 'oracle'.
           'NAME': 'refugeebuddy',                      # Or path to database file if using sqlite3.
           'USER': 'refugeebuddy',                      # Not used with sqlite3.
           'PASSWORD': 'postgres_Fug33s!!',                  # Not used with sqlite3.
           'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
           'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Australia/Sydney'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-au'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../public/media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r==z1wfvptlj7#utl@$nn8+qi5#ojl2xvl&l(dp^4@90@$z3#v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, '../templates')
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    
    'accounts',
    'geolocation',
    
    'library',
    
    'buddies'
    
)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(PROJECT_ROOT, '../dev-log/emails') 
DEFAULT_FROM_EMAIL = 'test@email.com'

LOGIN_REDIRECT_URL = '/buddies/profiles/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'library.context_processors.setting_values',
)

geolocation_context = {
    "GEOLOCATION_DEFAULT_ADMINZOOM": 5,
    "GEOLOCATION_DEFAULT_POSITION": ("151.207114", "-33.867139") # Sydney
}

GOOGLE_MAPS_API_KEY = {
    'development': 'ABQIAAAAOAAK0DkG1Zh3gJ_8rsNzUxTpH3CbXHjuCVmaTc5MkkU4wO1RRhT8l12EFtzX9ndq-OKhzn6UV2XPoA', #127.0.0.1:8000
    'production': 'ABQIAAAAOAAK0DkG1Zh3gJ_8rsNzUxQYbUU02OONfD68M2kk19HZUAdQRRQhHCAeBexTOgKpZ_QjDjkSc1BhAA', #unsw.edu.au
}[environ]

# A buddy will be blacklisted after this many organisations flag him/her.
BUDDY_BLACKLIST_THRESHOLD = 1

