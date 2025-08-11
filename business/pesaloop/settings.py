from datetime import datetime, timedelta
import os
import environ
from pathlib import Path

# ====================
# PATH & ENV SETUP
# ====================

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(BASE_DIR / ".env")


# ====================
# APPLICATION METADATA
# ====================

APP_NAME = "PesaLoop"
APP_VERSION = "1.0.0"
COPYRIGHT_YEAR = datetime.now().year
PRIVACY_POLICY_URL = env("PRIVACY_POLICY_URL", default="#")
TERMS_URL = env("TERMS_URL", default="#")


# ====================
# CORE DJANGO SETTINGS
# ====================

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ====================
# URL CONFIGURATION
# ====================

ROOT_URLCONF = 'pesaloop.urls'
WSGI_APPLICATION = 'pesaloop.wsgi.application'

# Local/Production URLs
FRONTEND_LOCAL_URL = env('FRONTEND_LOCAL_URL')
BACKEND_LOCAL_URL = env('BACKEND_LOCAL_URL')
FRONTEND_PRODUCTION_URL = env('FRONTEND_PRODUCTION_URL')
BACKEND_PRODUCTION_URL = env('BACKEND_PRODUCTION_URL')


# ====================
# INTERNATIONALIZATION
# ====================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ====================
# STATIC FILES
# ====================

STATIC_URL = 'static/'


# ====================
# CUSTOM USER MODEL
# ====================

AUTH_USER_MODEL = 'userservice.User'


# ====================
# TEMPLATES
# ====================

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / "templates"],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]


# ====================
# INSTALLED APPS
# ====================

INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party base/libs
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # Database/async related
    'django_celery_results',
    'django_celery_beat',

    # Monitoring/auditing
    'easyaudit',

    # API documentation
    'drf_spectacular',
    'drf_spectacular_sidecar',

    # Custom apps
    'authservice',
    # 'cardservice',
    'creditservice',
    'data_encryption',
    'forexservice',
    'mediaservice',
    'mpesaservice',
    'paymentservice',
    'rbac',
    'reportingservice',
    'tracking',
    'userservice',
    'walletservice',
]

# Development-only apps
if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
        # other dev-only apps
    ]

# ====================
# MIDDLEWARE
# ====================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


# ====================
# DATABASE CONFIGURATION
# ====================

DB_KEYS = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']

if all(env(key) for key in DB_KEYS):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / f'artifacts/{APP_NAME.lower()}.sqlite3',
        }
    }


# ====================
# PASSWORD VALIDATION
# ====================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ====================
# DJANGO REST FRAMEWORK
# ====================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rbac.permissions.MethodPermission',
        'rbac.permissions.SensitiveOperationPermission',
        'rbac.permissions.BusinessHoursAccessPermission',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'burst': '60/min',
        'sustained': '1000/hour',
        'user': '1000/day',
        'payment': '30/minute',
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


# ====================
# SIMPLE JWT
# ====================

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1500),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=100),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'BLACKLIST_AFTER_ROTATION': True,
    'ROTATE_REFRESH_TOKENS': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}


# ====================
# CORS HEADERS
# ====================

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:19006"
]
CORS_ALLOW_HEADERS = (
    "accept", "authorization", "content-type", "user-agent",
    "x-csrftoken", "x-requested-with",
)
CORS_ALLOW_METHODS = (
    "DELETE", "GET", "PATCH", "POST", "PUT",
)


# ====================
# EASYAUDIT
# ====================

DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = True
DJANGO_EASY_AUDIT_CRUD_EVENT_NO_CHANGED_FIELDS_SKIP = True
DJANGO_EASY_AUDIT_READONLY_EVENTS = True
DJANGO_EASY_AUDIT_CHECK_IF_REQUEST_USER_EXISTS = False


# ====================
# SECURITY TRACKING
# ====================

# Activity Tracking Settings
ACTIVITY_TRACKING = {
    'DISABLE_GEOLOCATION': False,
    'DISABLE_ASN_LOOKUP': False,
    'ASN_LOOKUP_TIMEOUT': 2,  # seconds
    'GEOLOCATION_TIMEOUT': 2,
    'SENSITIVE_FIELDS': ['password', 'token', 'secret', 'credit_card', 'cvv'],
    'DEFAULT_ACTIVITY_TYPE': 'OTHER',
}


# ====================
# EMAIL CONFIGURATION
# ====================

# --- Core SMTP Settings ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)
EMAIL_TIMEOUT = env.int('EMAIL_TIMEOUT', default=300)
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# --- Bulk Email Settings ---
EMAIL_BATCH_SIZE = env.int('EMAIL_BATCH_SIZE', default=100)
EMAIL_BATCH_DELAY = env.int('EMAIL_BATCH_DELAY', default=30)

# --- Email Address Roles ---
EMAIL_FROM_ALERTS = f"{APP_NAME} <{env('EMAIL_ALERTS')}>"
EMAIL_SUPPORT = env('EMAIL_SUPPORT')
EMAIL_REPLY_TO = env('EMAIL_REPLY_TO')
EMAIL_SYS_ADMIN = env('EMAIL_SYS_ADMIN')
EMAIL_SECURITY = env('EMAIL_SECURITY')


# ====================
# CELERY
# ====================

CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CONNECTION_MAX_RETRIES = 10


# ====================
# DATA ENCRYPTION
# ====================

DB_ENCRYPTION_KEY = env('DB_ENCRYPTION_KEY')
PAYLOAD_ENCRYPTION_KEY = env('PAYLOAD_ENCRYPTION_KEY')
ENCRYPTION_KEY_ROTATION = {
    'BACKUP_DIR': BASE_DIR / 'common' / 'backups' / 'keys',
    'BACKUP_FILENAME_FORMAT': 'encryption_key_{timestamp}.json',
    'KEY_ROTATION_SCHEDULE': 'monthly'
}


# ====================
# THIRD-PARTY SERVICES
# ====================

# Twilio
TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN')
TWILIO_SMS_FROM = env('TWILIO_SMS_FROM')

# Exchange Rates API
EXCHANGE_API_URL = env('EXCHANGE_API_URL')
EXCHANGE_API_KEY = env('EXCHANGE_API_KEY')

# M-Pesa
MPESA_TOKEN_ENDPOINT = env('MPESA_TOKEN_ENDPOINT')
MPESA_STK_PUSH_ENDPOINT = env('MPESA_STK_PUSH_ENDPOINT')
MPESA_CONSUMER_KEY = env('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = env('MPESA_CONSUMER_SECRET')
MPESA_PASSKEY = env('MPESA_PASSKEY')
MPESA_TRANSACTION_TYPE = env('MPESA_TRANSACTION_TYPE', default='CustomerPayBillOnline')
MPESA_BUSINESS_SHORTCODE = env('MPESA_BUSINESS_SHORTCODE')
MPESA_PARTY_B_SHORTCODE = env('MPESA_PARTY_B_SHORTCODE')
MPESA_CALLBACK_URL = BACKEND_LOCAL_URL + "/api/mpesaservice/stk-push/callback"
DARAJA_CALLBACK_SECRET_TOKEN = env('DARAJA_CALLBACK_SECRET_TOKEN')


# ====================
# LOGGING
# ====================

APPLICATION_LOG_FILEPATH = str(BASE_DIR / 'common' / 'artifacts' / 'logs' / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': APPLICATION_LOG_FILEPATH,
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}


# ====================
# DRF SPECTACULAR
# ====================

SPECTACULAR_SETTINGS = {
    'TITLE': f'{APP_NAME} API',
    'DESCRIPTION': (
        f'Comprehensive API documentation for the {APP_NAME} platform.\n\n'
        'Includes services for:\n'
        '- User onboarding and KYC\n'
        '- Wallet and transaction management\n'
        '- Mobile money (M-Pesa) integration\n'
        '- Card processing (planned)\n'
        '- Forex currency exchange\n'
        '- Credit issuance\n'
        '- Reporting & analytics\n'
        '- Secure biometric & credential auth\n'
    ),
    'VERSION': '1.5.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    'REDOC_SETTINGS': {
        'lazyRendering': True,
    },
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
    'AUTHENTICATION_WHITELIST': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'ENUM_NAME_OVERRIDES': {},
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.hooks.postprocess_schema_enums',
    ],
    'DISABLE_ERRORS_AND_WARNINGS': False,
    'GENERIC_ADDITIONAL_PROPERTIES': None,
    'SCHEMA_COERCE_PATH_PK_SUFFIX': True,
    'SCHEMA_PATH_PREFIX_TRIM': False,
    'SECURITY': [
        {
            'JWT': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'JWT authentication using the Bearer scheme. Example: "Authorization: Bearer {token}"',
            }
        },
    ],
    'PREPROCESSING_HOOKS': [
        'drf_spectacular.hooks.preprocess_exclude_path_format',
    ],
}


# ====================
# DEBUG TOOLBAR
# ====================

INTERNAL_IPS = ['127.0.0.1', 'localhost']
