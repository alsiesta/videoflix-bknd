from datetime import timedelta
from pathlib import Path
from re import DEBUG
from unittest.mock import DEFAULT
from dotenv import load_dotenv
import os


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# DEBUG = True

# Load environment variables
DJANGO_ENV = os.getenv('DJANGO_ENV')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'
DEV_HOST = os.getenv('DEV_HOST')
PROD_HOST = os.getenv('PROD_HOST')
DEV_REDIS_HOST = os.getenv('DEV_REDIS_HOST')
PROD_REDIS_HOST = os.getenv('PROD_REDIS_HOST')

# Common settings
SECRET_KEY = 'django-insecure-vujvv1ruvhk_p_67cz^v!x7oztsqgv0ech(ns2=^t90xzb1s=^'


# Printing environment variables
def print_env_vars():
    print("DJANGO_ENV:", DJANGO_ENV)
    print("DEBUG:", DEBUG)
    print("DEV_HOST:", DEV_HOST)
    print("PROD_HOST:", PROD_HOST)
    print("DEV_REDIS_HOST:", DEV_REDIS_HOST)
    print("PROD_REDIS_HOST:", PROD_REDIS_HOST)
    print("ALLOWED_HOSTS:", ALLOWED_HOSTS)
    print("FRONTEND_HOST:", FRONTEND_HOST)
    print("CORS_ALLOWED_ORIGINS:", CORS_ALLOWED_ORIGINS)
    
    
if DEBUG:
    ALLOWED_HOSTS = [DEV_HOST, '127.0.0.1', 'localhost', 'localhost:4200']
    FRONTEND_HOST = os.getenv('FRONTEND_HOST_DEV', 'http://localhost:4200')
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:4200'
    ]
    # print_env_vars()
else:
    ALLOWED_HOSTS = [PROD_HOST, 'your-production-domain.com']
    FRONTEND_HOST = os.getenv('FRONTEND_HOST_PROD', 'https://videoflix.alsiesta.com')
    CORS_ALLOWED_ORIGINS = [
        'https://videoflix.alsiesta.com'
    ]
    # print_env_vars()



CSRF_TRUSTED_ORIGINS = [
    'http://localhost:4200', 'https://videoflix.alsiesta.com',
]

INTERNAL_IPS = ["127.0.0.1"]

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
    'user.apps.UserConfig',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'user', 'templates'),
            os.path.join(BASE_DIR, 'videoflixbknd', 'templates')
        ],
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

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'videoflix_db',
		'USER': 'postgres',
		'PASSWORD': 'Test123',
		'HOST': 'localhost',
		'PORT': '5432',
	}
}

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


AUTH_USER_MODEL = 'user.CustomUser'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

mail = os.getenv('EMAIL_HOST_USER')
mail_pass = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = mail
EMAIL_HOST_PASSWORD = mail_pass

DEFAULT_FROM_EMAIL = 'noreply<no_reply@domain.com>'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL= '/'

CACHE_TTL = 0

if DJANGO_ENV == 'production':
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': f'redis://{PROD_REDIS_HOST}:6379/1',
            'OPTIONS': {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": "videoflix"
        }
    }

    RQ_QUEUES = {
        'default': {
            'URL': f'redis://{PROD_REDIS_HOST}:6379/0',
            'HOST': PROD_REDIS_HOST,
            'PORT': 6379,
            'DB': 0,
            'DEFAULT_TIMEOUT': 360,
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': f'redis://{DEV_REDIS_HOST}:6379/1',
            'OPTIONS': {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": "videoflix"
        }
    }

    RQ_QUEUES = {
        'default': {
            'URL': f'redis://{DEV_REDIS_HOST}:6379/0',
            'HOST': DEV_REDIS_HOST,
            'PORT': 6379,
            'DB': 0,
            'DEFAULT_TIMEOUT': 360,
        }
    }
