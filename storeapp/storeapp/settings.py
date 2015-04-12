6374# -*- encoding: utf-8 -*-
"""
Django settings for storeapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


import os
#comentar esta linea para hacer funcionar los routers, nstalar pip install django-routers
#from django.db import connections

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '38&ogn3&^g$&6!2+l(b#ma87(oif(y4#0_bt1ourjop!3k3zss'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
APPEND_SLASH = False



ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'gunicorn',
    'store',
    'admin',
    'clientes',
    'cms',
    'yopi',
)


MIDDLEWARE_CLASSES = (
    'middleware.MultiSiteMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
)
HOST_MIDDLEWARE_URLCONF_MAP = {
    # Control Panel
    "www.wido.mx": "wido.mx",
}


ROOT_URLCONF = 'storeapp.urls'

WSGI_APPLICATION = 'storeapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'tienda',
        'USER': 'root',
        'PASSWORD': '6374',
        'STORAGE_ENGINE': 'INNODB',
        'OPTIONS': {
                       'init_command': 'SET storage_engine=INNODB',
                    },
        'CHARSET':'',
        'HOST':'127.0.0.1'
    },
    'usuario': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'usuario',
        'USER': 'root',
        'PASSWORD': '6374',
        'STORAGE_ENGINE': 'INNODB',
        'CHARSET':'',
        'HOST':'127.0.0.1'
    },
    'cms': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'cms',
        'USER': 'root',
        'PASSWORD': '6374',
        'STORAGE_ENGINE': 'INNODB',
        'CHARSET':'',
        'HOST':'127.0.0.1'
    },
    'client': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'client',
        'USER': 'root',
        'PASSWORD': '6374',
        'STORAGE_ENGINE': 'INNODB',
        'CHARSET':'',
        'HOST':'127.0.0.1'
    },
}



DATABASE_ROUTERS = ['cms.router.cms','store.router.Store','clientes.router.Client', 'admin.router.AdminRouter','storeapp.router.MasterSlaveRouter']
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

#STATIC_ROOT=os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]+['static'])
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
#STATICFILES_STORAGE ='django.contrib.staticfiles.storage.CachedStaticFilesStorage'



#STATIC_ROOT= '/static/'
#MEDIA_ROOT = 'static/imagenes/tiendas/'
MEDIA_ROOT=os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]+['static/imagenes/tiendas/'])

MEDIA_URL  = '/media/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'mail.aristasoluciones.com'
EMAIL_HOST_USER     = 'wido@aristasoluciones.com'
EMAIL_HOST_PASSWORD = 'nub3w3b&2'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
STATIC_ROOT = "static/"
STATIC_URL='/static/'
#STATIC_URL = 'http://elcafecito.com.mx/statics/'
#STATIC_URL='/static/'


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

