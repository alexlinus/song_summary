"""
Django settings for song_summary project.

Generated by "django-admin startproject" using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import environ
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="some_key")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.summarizer",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("REDIS_URL", default="redis://localhost:6379/1"),
        # "OPTIONS": {
        #     "CLIENT_CLASS": "django_redis.client.DefaultClient",
        # }
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---- Cache timeouts ----

MUSIX_MATCH_CACHE_TIMEOUT_SECONDS = env.int("MUSIX_MATCH_CACHE_TIMEOUT_SECONDS", default=3600)
OPEN_AI_CACHE_TIMEOUT_SECONDS = env.int("OPEN_AI_CACHE_TIMEOUT_SECONDS", default=3600)


# ---- API KEYS ----

# GPT API KEY to analyze lyrics and extract data
OPEN_AI_API_KEY = env.str("OPEN_AI_API_KEY", default="some_key")

# Music Match API key, to get lyrics
MUSIX_MATCH_API_KEY = env.str("MUSIX_MATCH_API_KEY", default="some_key")


# ---- API settings ----

MUSIX_MATCH_BASE_API_URL = env.str(
    "MUSIX_MATCH_BASE_API_URL",
    default="https://api.musixmatch.com/ws/1.1/matcher.lyrics.get",
)

GPT_MODEL = env.str("GPT_MODEL", default="gpt-3.5-turbo-0125")


# ---- GPT PROMPTS ----

GPT_SUMMARIZE_LYRICS_PROMPT = env.str(
    "GPT_SUMMARIZE_LYRICS_PROMPT",
    default="Summarize the following song lyrics in one sentence:\n\n{lyrics}",
)

GPT_EXTRACT_COUNTRIES_PROMPT = env.str(
    "GPT_EXTRACT_COUNTRIES_PROMPT",
    default="List any countries mentioned in the following song lyrics:\n\n{lyrics}"
)