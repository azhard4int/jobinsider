"""
Django settings for jobsinsider_app project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from unipath import Path

BASE_DIR = Path(__file__).ancestor(2)
# STATIC_ROOT = BASE_DIR.child('assets')
MEDIA_ROOT = str(BASE_DIR.child('media'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gq+6u=92e#i#_&yk-#g75iinbcew+z8mcly7p*pcl@8s(%clv='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'twitter_bootstrap',
    'accounts',
    'core',
    'users',
    'private',
    'company',
    'bootstrap3',
    'redactor',
    'tinymce'
    # 'ajax_upload'
    )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'jobsinsider_app.urls'


# Accounts directory
TEMP_DIRECTORY_REGISTER = [
    'templates/accounts/registration',
]

# Admindirectory
TEMP_DIRECTORY_ADMIN = [
    'templates/accounts/admin',
]

# Email Templates for Accounts
TEMP_DIRECTORY_EMAILS = [
    'templates/accounts/emails',
]

# Inner Dashboard
TEMP_DIRECTORY_Dashboard = [
    'templates/accounts/dashboard',
]
TEMP_DIRECTORY_Dashboard_other = [
    'templates/accounts/dashboard',
]



# Profile Directory

TEMP_DIRECTORY_Dashboard = [
    'templates/accounts/profile',
]


# Private Zone
TEMP_DIRECTORY_PRIVATE = [
    'templates/private',
]

# Company Dashboard
TEMP_DIRECTORY_Company = [
    'templates/company',
]

# Company Jobs
TEMP_DIRECTORY_JOBS = [
    'templates/jobs',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            BASE_DIR.child('templates'),
            BASE_DIR.join(TEMP_DIRECTORY_REGISTER),
            BASE_DIR.join(TEMP_DIRECTORY_EMAILS),
            BASE_DIR.join(TEMP_DIRECTORY_ADMIN),
            BASE_DIR.join(TEMP_DIRECTORY_PRIVATE),
            BASE_DIR.join(TEMP_DIRECTORY_Dashboard),
            BASE_DIR.join(TEMP_DIRECTORY_Dashboard_other),
            BASE_DIR.join(TEMP_DIRECTORY_Company),
            BASE_DIR.join(TEMP_DIRECTORY_JOBS),
        ),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.core.context_processors.media",
                "django.core.context_processors.static",
            ],
        },
    },
]

WSGI_APPLICATION = 'jobsinsider_app.wsgi.application'


TEMPLATE_DIRS = (


)

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jobsinsider',
        'USER': 'root',
        'PASSWORD': 'gonein60sec',
        'HOST': 'localhost',
        'PORT': '3306',
        }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, 'assets/css/'),
    # os.path.join(BASE_DIR, 'assets/js/'),
    # # os.path.join(BASE_DIR,'css'),

    BASE_DIR.child("assets"),
    # BASE_DIR.child("js"),
    # BASE_DIR.child("static"),
)

STATIC_ROOT = ''
# STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATIC_URL = '/assets/'
MEDIA_URL = '/media/'
# Email Configuration

EMAIL_HOST = 'smtp.critsend.com'
EMAIL_HOST_USER = 'waqar@techpointmedia.com'
EMAIL_HOST_PASSWORD = 'nC5pDMz6cC8W2'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

TINYMCE_JS_URL = 'http://debug.example.org/tiny_mce/tiny_mce_src.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True