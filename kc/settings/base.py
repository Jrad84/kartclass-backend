"""
Django settings for ds_karting project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from datetime import timedelta
import os
import django_heroku
import dj_database_url
from dj_database_url import parse as db_url
from decouple import config


# root = environ.Path(__file__) - 3  



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DEBUG = False

# add the following just below STATIC_URL
MEDIA_URL = '/media/'  # add this
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # add this

ROOT_URLCONF = 'kc.urls'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
     "81281f4fbf47.ngrok.io",
     "localhost",
     "kartclass-django/herokuapp.com",
     "kartclass-nuxt/herokuapp.com"
     ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'kc.core',
    'kc.api',
    'kc.accounts',
    'corsheaders',
    'django_filters',
    'rest_registration',
    'stripe',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# EMAIL settings
# EMAIL_HOST=config('EMAIL_HOST')
# EMAIL_HOST_USER=config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD=config('EMAIL_HOST_PASSWORD')
# EMAIL_PORT=config('EMAIL_PORT')
# EMAIL_USE_TLS=config('EMAIL_USE_TLS')
# EMAIL_USE_SSL=config('EMAIL_USE_SSL')



# DRF stuff.
REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': ( 
       
        'rest_framework.permissions.IsAuthenticated',
         ),

   'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

}

# https://django-rest-registration.readthedocs.io/en/latest/quickstart.html
REST_REGISTRATION = {
    'REGISTER_VERIFICATION_ENABLED': True,
    'REGISTER_EMAIL_VERIFICATION_ENABLED': True,
    'RESET_PASSWORD_VERIFICATION_ENABLED': True,
    'REGISTER_VERIFICATION_URL': 'https://127.0.0.1:3000/verify-user/',
    'RESET_PASSWORD_VERIFICATION_URL': 'https://127.0.0.1:3000/reset-password/',
    'REGISTER_EMAIL_VERIFICATION_URL': 'https://127.0.0.1:3000/verify-email/',

    'VERIFICATION_FROM_EMAIL': 'jaredtaback@gmail.com',
    
    "USER_DETAILS_SERIALIZER": "api.v1.serializers.user.UserRetrieveSerializer",
    'REGISTER_SERIALIZER_CLASS': 'api.v1.serializers.user.UserCreateSerializer',
}


JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': timedelta(hours=1),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('JWT',),
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles'),
STATIC_URL = '/static/'

CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.dev.json'),
    }
}

AUTH_USER_MODEL = 'accounts.CustomUser'

# CORS stuff.
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# STRIPE 
STRIPE_SECRET_KEY=config('STRIPE_SECRET_KEY')

# Heroku: Update database configuration from $DATABASE_URL.

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='postgres://USER:PASSWORD@HOST:PORT/NAME',
        cast=db_url
    )
}

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)



# Activate Django-Heroku.
django_heroku.settings(locals())
