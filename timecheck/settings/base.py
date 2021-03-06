"""
Django settings for TimeCheck project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$x-&way2+s1rn3qlxw29uvl%k_xe*aj2li9hf=ty5(bjl8=m7r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'groups.apps.GroupsConfig',
    'events.apps.EventsConfig',
    'activities.apps.ActivitiesConfig',
    'polls.apps.PollsConfig',
    # 'calendars.apps.CalendarsConfig',
    'notes.apps.NotesConfig',
    'rest_framework',
    'knox',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'timecheck.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../../templates')]
        ,
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

WSGI_APPLICATION = 'timecheck.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'timecheck',
        'HOST': 'localhost',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


AUTH_USER_MODEL = 'users.User'

APPEND_SLASH = False

AUTH_JWT_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArJ61NQ3dBlEXu44vO0Jd
E+9OeToAxG+11a6ghGA7MPjwK/i8dBDDE0a1Q1qTukGwaoM3kq2MPCmyJ/g2hNGZ
uC5baINa27x2s6Fg5UC/GE1o29cnM8ZBSEovmYg52/4CTvGm8ZPaexhntkHbFUl4
tsuDIGzRX0p3qRNVuNiqZNj+auvBz4M8CoxlNaOtS7QS2LMfKvdZN7ZfH4WlDXK7
d8ceLb1zrxzPSrMXDmOgd1L6YAVrr1cu94nz3sBWf6h/tynmAPjop+XufICwx0OW
p3x1L1xy5JiQGBrvp/wBwxDpUz9/wk5MOngPWh67jGRTb5gjc+Qc+INtT4JLVJ5/
YJgAPEc0MoUZFDh2MexsNwIXgAbbL8j6eNZKtF/jwiR2RPRJdW+b8rCKUZpaYaRw
wB8mPlXF+THBGlK2AHZQlChwUlnixu5irjylwZRqqWhBZXFXELWoXTwFLX6fY69c
jGOOcgGNr226wDjiC7P/oiLuQrWfxM+n6dyDHX/UOctaqTwcHLraLrbggFSRE0jn
S/TCwzEWIL2yarLc5ucym+nopXTqSdKP4hj8hOhHT3vwmXKWznlrALdvDsR/Mlrf
2rp/qGS6BP4tpvqrNtEWa6g8ueCn6nTh9arU9nZOyjY9wgKtM3dM6mh5AlRSvx0I
PvSY+j8PT75/gZ3GZG6unSMCAwEAAQ==
-----END PUBLIC KEY-----"""

AUTH_JWT_OPTIONS = {
    "verify_signature": True,
    "verify_aud": True,
    "verify_iat": True,
    "verify_exp": True,
    "verify_nbf": False,
    "verify_iss": True,
    "verify_sub": True,
    "verify_jti": False,
    "verify_at_hash": False,   # JWT Access Tokens not used
    "leeway": 0,
}

AUTH_JWT_VALID_ALGORITHMS = ("RS256", "RS512",)

REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 128,
    'TOKEN_TTL': timedelta(days=31),
    'USER_SERIALIZER': None,
    'TOKEN_LIMIT_PER_USER': None,
    'AUTO_REFRESH': True,
    'MIN_REFRESH_INTERVAL': timedelta(days=1).total_seconds(),
    'AUTH_HEADER_PREFIX': 'Token',
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    # 'PAGE_SIZE': 50
}

CORS_ORIGIN_ALLOW_ALL = True

