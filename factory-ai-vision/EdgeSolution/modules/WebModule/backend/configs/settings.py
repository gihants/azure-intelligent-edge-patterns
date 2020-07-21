"""Django settings for vision_on_edge project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

import config
from configs import logging_config
from configs.app_insight import APP_INSIGHT_ON
from configs.customvision_config import ENDPOINT, TRAINING_KEY

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Project root
PROJECT_ROOT = BASE_DIR + '/vision_on_edge'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gjfeo_pt@1$23c$*g8to4bewom59sml0%8fgbdgot=ypr84b$@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'channels',
    'vision_on_edge.azure_parts',
    'vision_on_edge.images',
    'vision_on_edge.streams',
    'vision_on_edge.azure_settings',
    'vision_on_edge.feedback',
    'vision_on_edge.locations',
    'vision_on_edge.cameras',
    'vision_on_edge.image_predictions',
    'vision_on_edge.azure_training',
    'vision_on_edge.notifications',
    'rest_framework',
    'drf_yasg',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if APP_INSIGHT_ON:
    from configs.app_insight import APP_INSIGHT_CONN_STR
    MIDDLEWARE.append('opencensus.ext.django.middleware.OpencensusMiddleware')
    OPENCENSUS = {
        'TRACE': {
            'SAMPLER':
                'opencensus.trace.samplers.ProbabilitySampler(rate=1)',
            'EXPORTER':
                f'''opencensus.ext.azure.trace_exporter.AzureExporter(
                connection_string="{APP_INSIGHT_CONN_STR}"
            )''',
        }
    }

ROOT_URLCONF = 'configs.urls'

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

CORS_ORIGIN_ALLOW_ALL = True

ASGI_APPLICATION = 'configs.routing.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

UI_DIR = os.path.join(PROJECT_ROOT, 'ui_production')
STATICFILES_DIRS = [
    os.path.join(UI_DIR, 'static'),
]

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

ICON_URL = '/icons/'
ICON_ROOT = os.path.join(UI_DIR, 'icons')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

IOT_HUB_CONNECTION_STRING = config.IOT_HUB_CONNECTION_STRING
DEVICE_ID = config.DEVICE_ID
MODULE_ID = config.MODULE_ID

print('************************************')
print('CONFIGURATION:')
print('  TRAINING_KEY:', TRAINING_KEY)
print('  ENDPOINT:', ENDPOINT)
print('************************************')

LOGGING = logging_config.LOGGING_CONFIG_DEV
