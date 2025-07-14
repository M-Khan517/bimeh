import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

from .template import TEMPLATE_CONFIG, THEME_LAYOUT_DIR, THEME_VARIABLES

load_dotenv()  # take environment variables from .env.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    default="django-insecure-_&ca+aoy0#q(#!aj88nf@#3^i%_cfv^b0&afgsf@)+1-zgms@5",
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True").lower() in ["true", "yes", "1"]


# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# Current DJANGO_ENVIRONMENT
ENVIRONMENT = os.environ.get("DJANGO_ENVIRONMENT", default="local")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "jalali_date",
    "import_export",
    "iranian_cities",
    "apps.account_module",
    "apps.home_module",
    "apps.insurance_module",
    "apps.payment_module",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
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
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.language_code",
                "config.context_processors.my_setting",
                "config.context_processors.get_cookie",
                "config.context_processors.environment",
            ],
            "libraries": {
                "theme": "web_project.template_tags.theme",
            },
            "builtins": [
                "django.templatetags.static",
                "web_project.template_tags.theme",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # }
    
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'mydb',
    #     'USER': '',
    #     'PASSWORD': '',
    #     'HOST':'localhost',
    #     'PORT':'3306',
    # }
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "bimeh_db",
        "USER":"root",
        "PASSWORD":"32769272",
    }
}

AUTH_USER_MODEL = "account_module.User"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# Enable i18n and set the list of supported languages
LANGUAGES = [
    # ("en", _("English")),
    # ("fr", _("French")),
    # ("ar", _("Arabic")),
    # ("de", _("German")),
    ("fa", _("Farsi")),
    # Add more languages as needed
]

# Set default language
# ! Make sure you have cleared the browser cache after changing the default language
LANGUAGE_CODE = "fa"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "locale",
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "src" / "assets" / "upload"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "src" / "assets",
]


# Default URL on which Django application runs for specific environment
BASE_URL = os.environ.get("BASE_URL", default="http://127.0.0.1:8000")

LOGIN_URL = f"{BASE_URL}/auth/login"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Template Settings
# ------------------------------------------------------------------------------

THEME_LAYOUT_DIR = THEME_LAYOUT_DIR
TEMPLATE_CONFIG = TEMPLATE_CONFIG
THEME_VARIABLES = THEME_VARIABLES

# Your stuff...
# ------------------------------------------------------------------------------


# melipayamak config

MELI_USERNAME = "09338033497"
MELI_PASSWORD = "c86g5"

# font for pdf

# iranian cities

IRANIAN_CITIES_ADMIN_ADD_READONLY_ENABLED = False
IRANIAN_CITIES_ADMIN_DELETE_READONLY_ENABLED = False
IRANIAN_CITIES_ADMIN_CHANGE_READONLY_ENABLED = False
IRANIAN_CITIES_ADMIN_INLINE_ENABLED = False

FONT_PATH = os.path.join(BASE_DIR, "src/fonts/Vazir-Black-FD.ttf")

# jalali


# default settings (optional)
JALALI_DATE_DEFAULTS = {
    # if change it to true then all dates of the list_display will convert to the Jalali.
    "LIST_DISPLAY_AUTO_CONVERT": True,
    "Strftime": {
        "date": "%y/%m/%d",
        "datetime": "%H:%M:%S _ %y/%m/%d",
    },
    "Static": {
        "js": [
            "admin/js/django_jalali.min.js",
        ],
        "css": {
            "all": [
                "admin/css/django_jalali.min.css",
            ]
        },
    },
}


# zarin pall
# SANDBOX MODE

MERCHANT = "1efb04a1-f492-44b1-bfea-6cca8523520b"


SANDBOX = False
