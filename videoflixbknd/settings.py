"""
Django settings for videoflixbknd project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
from re import DEBUG
from unittest.mock import DEFAULT
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vujvv1ruvhk_p_67cz^v!x7oztsqgv0ech(ns2=^t90xzb1s=^'


# DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'
# DEV_HOST = os.getenv('DEV_HOST', '127.0.0.1')
# PROD_HOST = os.getenv('PROD_HOST', 'your-production-domain.com')

# if DEBUG:
#     ALLOWED_HOSTS = [DEV_HOST, '127.0.0.1', 'localhost','localhost:4200']
# else:
#     ALLOWED_HOSTS = [PROD_HOST, 'your-production-domain.com']
DEBUG = True


FRONTEND_HOST = os.getenv('FRONTEND_HOST')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'localhost:4200']

# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:4200',
#     'http://127.0.0.1:3000',
#     'http://localhost:3030',
# ]
# Application definition
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:4200',
]


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'videos.apps.VideosConfig',
    "verify_email.apps.VerifyEmailConfig",
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_rq',
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

ROOT_URLCONF = 'videoflixbknd.urls'

CACHE_TTL = 60 * 15

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://172.28.165.239:6379/1',
        'OPTIONS': {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "videoflix"
    }
}

RQ_QUEUES = {
    'default': {
        'URL': 'redis://172.28.165.239:6379/0',
        'HOST': '172.28.165.239',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    }
}

# RQ_EXCEPTION_HANDLERS = ['path.to.my.handler'] # If you need custom exception handlers



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'user', 'templates')],
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

WSGI_APPLICATION = 'videoflixbknd.wsgi.application'

# below sets authentication for each view globally. Which means that every view will require authentication unless explicitly stated otherwise setting empty @authentication_classes([]) and @permission_classes([]) per view
REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}



# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = 'static/'
# STATICS_DIRS = [BASE_DIR / 'static']
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Mail configuration
mail = os.getenv('EMAIL_HOST_USER')
mail_pass = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
EMAIL_HOST_USER = mail
EMAIL_HOST_PASSWORD = mail_pass

# DEFAULT_FROM_EMAIL = mail #recommended in video from Piko can Fly (https://www.youtube.com/watch?v=UV3bZbfEizo&t=221s)
DEFAULT_FROM_EMAIL = 'noreply<no_reply@domain.com>' #recommended from Django Verify Email (https://pypi.org/project/Django-Verify-Email/)


LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL= '/'

# #use this for the email verification, if you don't want to setup the smtp server
# #this will print the email exchange in the console for debugging
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
