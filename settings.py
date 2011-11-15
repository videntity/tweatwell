#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

# Django settings for tweatwell project.
import os, sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alan Viars', 'aviars@videntity.com'),
)
SITE_ID = 1
MANAGERS = ADMINS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://tweatwell.s3.amazonaws.com/media/'
MEDIA_URL = 'http://127.0.0.1/media/'

#Use a custom authentication backend to allow login with username or email.
AUTHENTICATION_BACKENDS = (
    'tweatwell.accounts.email-auth.EmailBackend',
 )


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'https://videntitystatic.s3.amazonaws.com/admin/media/'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cw87b^k4+bl#-jj#gf3)%&!^k@fr_j4#p8g@uoyn!ijzmnce1i'


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/'


ROOT_URLCONF = 'tweatwell.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.auth',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'tweatwell.web',
    'tweatwell.web.twitbot',
    'tweatwell.web.coachespoll',
    'tweatwell.web.pointsrank',
    'tweatwell.web.awards',
    'tweatwell.web.questionstips',
    'tweatwell.web.foodreport',
    'tweatwell.web.givepoints',
    'tweatwell.accounts',
    'registration',
    'avatar',
    'django_ses',
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

EMAIL_HOST_USER = 'hive@videntity.com'
HOSTNAME_URL = 'http://tweatwell.com'
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'AKIAIE5XDCZ5PNK4RGOQ'
AWS_SECRET_ACCESS_KEY = '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'




#Registration Settings
ACCOUNT_ACTIVATION_DAYS = 2
#Only allow a person to registeration from this domain
#Set to None to allow any downa
#RESTRICT_REG_DOMAIN_TO="mix.wvu.edu"
RESTRICT_REG_DOMAIN_TO=None
MIN_PASSWORD_LEN=8

#Twitter Hash Tag.  Setting this gets only tweats with this hash.
#To turn off set yo None: TWITTERHASH=None
TWITTERHASH="wvu5"



#RESTCat Settings
RESTCAT_SERVER="http://restcat.tweatwell.com/"
RESTCAT_USER="tweatwellapp"
RESTCAT_PASS="tweatwellpass"
RESTCAT_USER_EMAIL="tweatwellapp@videntity.com"
DEFAULT_TRANSACTION_TIMEZONE_OFFSET=-5


