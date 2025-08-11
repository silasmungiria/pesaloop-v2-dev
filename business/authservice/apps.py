from django.apps import AppConfig
from django.conf import settings
from datetime import timedelta

class CredentialSecurityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authservice'
    verbose_name = 'Authentication Service'
