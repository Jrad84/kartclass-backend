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

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# add the following just below STATIC_URL
MEDIA_URL = '/media/'  # add this
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # add this

ROOT_URLCONF = 'kc.urls'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6o!xk51_#vyx*nu1opxm(2o&baaaw3)5@*2x3@a_2$xc3us)tj'

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
    'rest_framework',
    'core',
    'api',
    'accounts',
    'corsheaders',
    'django_filters',
    'rest_registration',
   

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
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kartclass',
        'USER': 'jarben',
        'PASSWORD': 'good_password',
        'HOST': 'localhost',
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

# DRF stuff.
REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     # By default we set everything to admin,
    #     #   then open endpoints on a case-by-case basis
        
    #      'rest_framework.permissions.IsAdminUser',
    #      'rest_framework.permissions.IsAuthenticated',
    # ),
    'DEFAULT_PERMISSION_CLASSES': ( 
       
        'rest_framework.permissions.IsAuthenticated',
         ),
    # 'TEST_REQUEST_RENDERER_CLASSES': (
    #     'rest_framework.renderers.MultiPartRenderer',
    #     'rest_framework.renderers.JSONRenderer',
    #     'rest_framework.renderers.TemplateHTMLRenderer'
    # ),
   'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 20,
}
# https://django-rest-registration.readthedocs.io/en/latest/quickstart.html
REST_REGISTRATION = {
    'REGISTER_VERIFICATION_ENABLED': False,
    'REGISTER_EMAIL_VERIFICATION_ENABLED': False,
    'RESET_PASSWORD_VERIFICATION_ENABLED': False,
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

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
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
