from django.db import models
from django.utils.translation import gettext_lazy as _

class ActivityType(models.TextChoices):
    AUTH = 'AUTH', _('Authentication')
    LOGIN = 'LOGIN', _('Login')
    LOGOUT = 'LOGOUT', _('Logout')
    PROFILE_VIEW = 'PROF_V', _('Profile View')
    PROFILE_EDIT = 'PROF_E', _('Profile Edit')
    PAYMENT = 'PAY', _('Payment')
    ADMIN = 'ADMIN', _('Admin Action')
    SYSTEM = 'SYSTEM', _('System Action')
    API_CALL = 'API', _('API Call')
    ERROR = 'ERROR', _('Error')
    OTHER = 'OTHER', _('Other')

class ActivityStatus(models.IntegerChoices):
    SUCCESS = 1, _('Success')
    FAILURE = 0, _('Failure')
    PENDING = 2, _('Pending')
