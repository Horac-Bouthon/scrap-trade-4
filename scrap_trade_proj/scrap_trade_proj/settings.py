"""
Django settings for scrap_trade_proj project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7v+3c-x48jc=2!6q5t)b$pmcd8q&(l4e2l8pr#j3@=k+n@1x@t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'customers.apps.CustomersConfig',
    'project_main.apps.ProjectMainConfig',
    'auction_house.apps.AuctionHouseConfig',
    'project_api.apps.ProjectApiConfig',
    'state_wf.apps.StateWfConfig',
    'integ.apps.IntegConfig',
    'doc_repo.apps.DocRepoConfig',
    'notification.apps.NotificationConfig',

    'crispy_forms',
    'rest_framework',
    'debug_toolbar',
    'django_cleanup.apps.CleanupConfig', #--- must be after all apps
]

MIDDLEWARE = [

    # Note: You should include the Debug Toolbar middleware as early as possible in the list. However, it must come after any other middleware that encodes the response’s content, such as GZipMiddleware.
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'scrap_trade_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Additions applied to every page's context
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',

                # Add the first project reference to the context of every page
                'project_main.context_processors.project',
            ],
        },
    },
]

WSGI_APPLICATION = 'scrap_trade_proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'cs'

LANGUAGES = [
    ('en', 'English'),
    ('de', 'German'),
    ('cs', 'Czech'),
]


USE_I18N = True  # Internationalization (multiple languages)


USE_L10N = False  # Localisation (data formatting based on culture)
DATE_FORMAT = "d.m.Y"
TIME_FORMAT = "H:i"
DATETIME_FORMAT = "d.m.Y H:i"



# Timezones
USE_TZ = True
TIME_ZONE = 'Europe/Prague'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

#STATIC_DIRS = [
#    os.path.join(BASE_DIR, 'staticfiles')
#]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'customers.ProjectCustomUser'
LOGIN_URL = 'user-login'  # Used by access view mixins + other builtin auth

CRISPY_TEMPLATE_PACK = 'bootstrap4'

INTERNAL_IPS = ['127.0.0.1']  # For limiting Debug Toolbar to dev

LOCALE_PATHS = ( os.path.join(BASE_DIR, 'locale'), )

THUMB_SIZE = (100, 100)


# Use local assets instead of CDN's.
# When in production, switch to False.
DEBUG_OFFLINE = False

# Production check
if DEBUG_OFFLINE and not DEBUG:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(
        "You can't have DEBUG_OFFLINE when not in debug"
    )


# application internal settings
AUTO_ANSWERS = True
DIRECT_ANSWER_ACCEPT = True
