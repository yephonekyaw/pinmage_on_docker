from .base import *

SECRET_KEY = "_8ORGATj9B_DOsqRxQn_8WxakcwdtbzKC14Pt9mR0Rk"

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
