"""AWS_ACCESS_KEYAWS_ACAWS_ACCESS_KEYAWS_ACCESS_KEYCESS_KEY
Django settings for need_deliver project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import json
envData = open(BASE_DIR + '/need_deliver/envData.json')  
envData = json.load(envData)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#ocpg)1w26_5!vp=e)zhly*x5taosu2o0x$+*&gmj!5m48dbsg'
MASTER_KEY='NTPvAIxaqaTUJ7WZzRvl8I+PhpMyxFoH'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.0.164', 'navsoft.co.in', '127.0.0.1', '18.215.17.207','9241fe2b.ngrok.io', 'needdeliver.com', 'www.needdeliver.com','192.168.0.235']


# Application definition
PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'rest_framework',
    'commonApp',
    'supplierRestApi',
    'driverRestApi',
    'webAdmin',
    'supplier',
    'customer',
    'driver',
]

OUTSIDE_APPS = [
    'storages',
    'corsheaders'
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS + OUTSIDE_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'google.com',
    'diaxrbad0p1f6.cloudfront.net'
)

ROOT_URLCONF = 'need_deliver.urls'

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# WSGI_APPLICATION = 'need_deliver.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
if envData['env_type'] == "Production":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'needdeliver',
            'USER': 'needdeliver',
            'PASSWORD': 'Needdeliver!234$', 
            'HOST': 'needdeliver.cn2vrmdn89gz.us-east-1.rds.amazonaws.com',
        }
    }
elif envData['env_type'] == "Staging":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'need_deliver',
            'USER': 'postgres',
            'PASSWORD': 'navsoftpsql',
            'HOST': '192.168.0.65',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'need_deliver',
            'USER': 'postgres',
            'PASSWORD': 'navsoftpsql',
            'HOST': '192.168.0.65',
        }
    }
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'need_deliver',
    #         'USER': 'postgres',
    #         'PASSWORD': 'Password1',
    #         'HOST': '127.0.0.1',
    #     }
    # }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240 
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
IS_ADMIN = 1
IS_SUPPLIER = 2
IS_DRIVER = 3
IS_CUSTOMER = 4


# ------------ AWS s3 bucket credentials ---------------
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = 'AKIAITKAFS4RRLBYHA6Q'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'needdeliverdev'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = 'diaxrbad0p1f6.cloudfront.net'

# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
AWS_LOCATION = 'static'


STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATIC_ROOT = '/%s/' % AWS_LOCATION
# STATIC_URL_TEMP = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# ------------ AWS s3 bucket credentials ---------------





SEGION_NAME = "us-east-1"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
BASE_URL = envData['base_url']
WEBADMIN_URL = BASE_URL 
NOTIFICATION_TYPE = {"booking_confirm":"BOOKING_CONFIRMED_FROM_DRIVER", "cross_overhead":"CROSSED_THRESHOLD", "new_booking":"NEW_BOOKING_AVAILABLE", 
"arrived_first_drop":"ARRIVED_AT_FIRST_LOCATION", "arrived_second_drop":"ARRIVED_AT_SECOND_LOCATION", "arrived_at_pickup":"ARRIVED_AT_PICKUP_LOCATION", "force_drop":"DROP_FORCEFULLY",
"cancelled_by_driver":"BOOKING_CANCELLED_BY_DRIVER", "cancelled_by_supplier":"BOOKING_CANCELLED_BY_SUPPLIER", "trip_completed":"TRIP_COMPLETED",
 "session_expired":"SESSION_EXPIRED","admin_push_notification":"ADMIN_PUSH_NOTIFY", "review_posted":"REVIEW_POSTED"}
# Mail settings
NO_REPLY_MAIL = "ishita@navsoft.in"

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ishita.basu@navsoft.in'
EMAIL_HOST_PASSWORD = 'zxcvbnm!@'

CONST_SPLASH_BANNER_TYPE = "BANNER"
ROOT_FLAGS_PATH = 'flags/'
FLAG_LARGE = ROOT_FLAGS_PATH + 'flags-large/'
FLAG_MEDIUM = ROOT_FLAGS_PATH + 'flags-medium/'
FLAG_SMALL = ROOT_FLAGS_PATH + 'flags-small/'
ORDER_PREFIX = "ND"

BOOKING_STATUS_PROCESSING = 1
BOOKING_STATUS_PLACED = 2
BOOKING_STATUS_CANCELLED = 3
BOOKING_STATUS_COMPLETED = 4
FCM_API_KEY = "AAAA-BZrTDk:APA91bFB7jw8hCehQbp6hRPFgSLLefUGMo45wsIZpEK3B5DWwB_W_0iJSZcQ25ZJ4tFbDvRJOXf6etVSCa9JMfRsrNWyVa7IZ2iOkh66HeBq356dDD6EGucn2NibweousjFKfVzhUOkV"
VEHICLE_BOOKING_RANGE = 20
FRONT_END_NO_OF_RECORD = 10
DRIVER_LOW_BALANCE_THRESHOLD = 100
# DRIVER_BOOKING_STAT
