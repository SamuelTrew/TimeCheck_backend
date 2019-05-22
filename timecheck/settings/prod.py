from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'timecheck',
        'USER': 'timecheck',
        'PASSWORD': 'LW5XXAV1qGg20iPMplOXRfpJ9H6IAlCu',
        'HOST': 'timecheck-do-user-4623094-0.db.ondigitalocean.com',
        'PORT': '25060',
    }
}

ALLOWED_HOSTS = ['.mtcp.io', '.mattcorp.com', '.timecheck.app']
