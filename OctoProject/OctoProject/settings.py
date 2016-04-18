"""
Django settings for OctoProject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

#emailsetup
EMAIL_USE_TLS=True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT=25
EMAIL_HOST_USER='resetISPP@gmail.com'
EMAIL_HOST_PASSWORD='chirag123'
DEFAULT_FROM_EMAIL = 'Octo Admin <noreply@Octoshape.com>'
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
LOGIN_URL = '/'
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEBUG = True
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nw3fv9jbq(#qr-e0)y*wohb^42c_sbth^-3vbvh5yw#mb(y0h$'

# SECURITY WARNING: don't run with debug turned on in production!

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates/'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
 #   'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'OctoProject.urls'

WSGI_APPLICATION = 'OctoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,'Octologs.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'login': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}