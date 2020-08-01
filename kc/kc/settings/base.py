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
import environ


# root = environ.Path(__file__) - 3  
env = environ.Env()
environ.Env.read_env()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# add the following just below STATIC_URL
MEDIA_URL = '/media/'  # add this
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # add this

ROOT_URLCONF = 'kc.urls'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = [
    "127.0.0.1",
     "81281f4fbf47.ngrok.io",
     "localhost",
     
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
    'core',
    'api',
    'accounts',
    'corsheaders',
    'django_filters',
    'rest_registration',
    'stripe',
   
   

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'pinax.stripe.middleware.ActiveSubscriptionMiddleware',
]


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

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('ENGINE'),
        'NAME': os.environ.get('NAME'),
        'USER': os.environ.get('USER'),
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': os.environ.get('HOST'),
        'PORT': '',
    }
}


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
EMAIL_HOST=os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER=os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT=os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS=os.environ.get('EMAIL_USE_TLS')
EMAIL_USE_SSL=os.environ.get('EMAIL_USE_SSL')



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

# ALLOWED_HOSTS = ("http://127.0.0.1:3000/",)

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
SITE_ID = 1
PINAX_STRIPE_DEFAULT_PLAN = ""
PAYMENT_PLANS = []
PINAX_STRIPE_SECRET_KEY = os.environ.get('PINAX_STRIPE_SECRET_KEY')
PINAX_STRIPE_PUBLIC_KEY = os.environ.get('PINAX_STRIPE_PUBLIC_KEY')
PINAX_STRIPE_INVOICE_FROM_EMAIL = os.environ.get('PINAX_STRIPE_INVOICE_FROM_EMAIL')
PINAX_STRIPE_SUBSCRIPTION_REQUIRED_EXCEPTION_URLS = []
PINAX_STRIPE_SUBSCRIPTION_REQUIRED_REDIRECT = ""
STRIPE_LIVE_MODE = False

# Activate Django-Heroku.
django_heroku.settings(locals())
