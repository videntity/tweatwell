#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

# Django settings for tweatwell project.
import os, sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    ('Alan Viars', 'aviars@videntity.com'),
)
SITE_ID = 1
MANAGERS = ADMINS

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cw87b^k4+bl#-jj#gf3)%&!^k@fr_j4#p8g@uoyn!ijzmnce1i'


# Fix up piston imports here. We would normally place piston in 
# a directory accessible via the Django app, but this is an
# example and we ship it a couple of directories up.
sys.path.insert(0, os.path.join(BASE_DIR, '../../'))

DBPATH = os.path.join(BASE_DIR, 'db/db.db')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DBPATH,                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
 }




# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://127.0.0.1:8000/media/'
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'
 
MAIN_STATIC_ROOT = os.path.join(BASE_DIR, 'mainstatic')
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    MAIN_STATIC_ROOT,
    )


#Use a custom authentication backend to allow login with username or email.

AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            )
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
LOGOUT_URL = '/accounts/logout'
LOGIN_URL='/accounts/login'
LOGIN_REDIRECT_URL = '/'


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


ROOT_URLCONF = 'tweatwell.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tweatwell.apps.twitbot',
    'tweatwell.apps.checkin',
    'tweatwell.apps.questions',
    'tweatwell.apps.roulette',
    'tweatwell.apps.recipes',
    'tweatwell.apps.tips',
    'tweatwell.apps.accounts',
    'tweatwell.apps.quiz',
    'tweatwell.apps.profile',
    'avatar',
    'django_ses',
    'sorl.thumbnail',
)



# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Email Settings --------------------------------------------------------------

EMAIL_HOST_USER = 'tweatwell@videntity.com'
HOSTNAME_URL = 'http://127.0.0.1:8000'
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'AKIAIU6C5F7PYXMGXKWA'
AWS_SECRET_ACCESS_KEY = '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'


RESTCAT_SERVER="127.0.0.1"
RESTCAT_USER=""
RESTCAT_PASS=""
# Registration  & Password Reset Settings --------------------------------------
# Only allow a person to registeration from this domain
# Set to None to allow any
# RESTRICT_REG_DOMAIN_TO="mix.wvu.edu"
RESTRICT_REG_DOMAIN_TO      = None
MIN_PASSWORD_LEN            = 8
SIGNUP_TIMEOUT_DAYS         = 7
PASSWORD_RESET_TIMEOUT_DAYS = 2 
ORGANIZATION_NAME           = "WVU:Tweatwell"


# Twitter Hash Tag.  Only fetch tweets with this hash.
# To turn off set to None: TWITTERHASH=None
TWITTERHASH="#freggie"

# TIMEZONE OFFSET
TIMEZONE_OFFSET=-5


try:
    from settings_local import *
except ImportError:
    pass

