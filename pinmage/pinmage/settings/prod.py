import os
from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

ADMINS = [
    ('Silly Boy', 'sillyboy.undercover@gmail.com'),
]

ALLOWED_HOSTS = ['www.pinmage.online', 'pinmage.online']

CSRF_TRUSTED_ORIGINS=['https://www.pinmage.online', 'https://pinmage.online']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
    }
}

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 30
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

