import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-pilot-key')

# SECURITY WARNING: don't run with debug turned on in production!
# Default to False for safety. Set DEBUG=True in your .env file for local development.
DEBUG = env('DEBUG')

# For production, set this to your Cloud Run service URL.
# For local dev, you can use 'localhost,127.0.0.1'.
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
RENDER_INTERNAL_HOSTNAME = env('RENDER_INTERNAL_HOSTNAME', default=None)
if RENDER_INTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_INTERNAL_HOSTNAME)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
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

# For production, restrict this to your frontend's domain.
# For local dev, set in .env: CORS_ALLOWED_ORIGINS=http://localhost:8080
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
# Allow all origins only if DEBUG is on and the list is empty
CORS_ALLOW_ALL_ORIGINS = not CORS_ALLOWED_ORIGINS and DEBUG

ROOT_URLCONF = 'pilot_backend.urls'

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

WSGI_APPLICATION = 'pilot_backend.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Use Cloud SQL if DATABASE_URL is set.
# This will raise an error if DATABASE_URL is not set in a non-DEBUG environment,
# preventing accidental use of SQLite in production. It will use SQLite if DEBUG is True and no URL is set.
DATABASES['default'] = env.db('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")

if DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
    DATABASES['default']['CONN_MAX_AGE'] = 600

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
