# Standard library imports
import uuid

# Django imports
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Project-specific imports
from .user_manager import userManager
from common import EncryptedFieldsMixin
from userservice.services import AccountNumberGenerator


class User(AbstractUser, PermissionsMixin, EncryptedFieldsMixin):
    # Disable default username, group, and permission handling
    username = None
    groups = None
    user_permissions = None

    # Unique identification
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("Unique system-wide identifier for the user.")
    )
    account_number = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        validators=[RegexValidator(r'^\d{10,20}$')],
        default=AccountNumberGenerator.generate,
        help_text=_("Unique account number assigned to the user.")
    )

    # Personal information
    first_name = models.CharField(
        max_length=255,
        help_text=_("User's first name.")
    )
    last_name = models.CharField(
        max_length=255,
        help_text=_("User's last name.")
    )
    email = models.EmailField(
        unique=True,
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                _('Enter a valid email address.')
            )
        ],
        help_text=_("A unique and valid email address.")
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                r'^\+[1-9]\d{1,14}$',
                _('Enter a valid international phone number (E.164 format).')
            )
        ],
        help_text=_("A unique phone number in E.164 international format (e.g., +2547...).")
    )
    country_code = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        help_text=_("ISO or custom country code for localization.")
    )

    # Authentication & security
    password = models.CharField(
        max_length=255,
        help_text=_("Hashed user password.")
    )
    password_reset_count = models.IntegerField(
        default=0,
        help_text=_("Number of times the user has reset their password.")
    )
    last_password_reset = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Timestamp of the last password reset.")
    )
    biometric_auth_enabled = models.BooleanField(
        default=False,
        help_text=_("Indicates if biometric authentication is enabled.")
    )

    # Verification flags
    is_loan_qualified = models.BooleanField(
        default=False,
        help_text=_("Indicates if the user is qualified to access loan products.")
    )
    verified_email = models.BooleanField(
        default=False,
        help_text=_("Indicates if the user's email is verified.")
    )
    verified_phone_number = models.BooleanField(
        default=False,
        help_text=_("Indicates if the user's phone number is verified.")
    )
    is_active = models.BooleanField(
        default=False,
        help_text=_("Designates whether this user should be treated as active.")
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_("Indicates if the user has passed verification/KYC.")
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text=_("Marks whether the user is soft-deleted from the system.")
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Timestamp when the user was soft-deleted.")
    )

    # Preferences
    use_sms = models.BooleanField(
        default=False,
        help_text=_("User's preference for receiving notifications via SMS or Email.")
    )

    # Authentication configuration
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = userManager()

    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email', 'phone_number', 'is_active', 'is_deleted']),
        ]
        default_permissions = ()  # Disable Django's built-in model permissions

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm_codename, method='ALL'):
        """
        Checks if user has the given permission through the custom RBAC system.
        """
        if self.is_superuser:
            return True
        from rbac.utils import check_permission
        return check_permission(self, perm_codename, method)

    def __str__(self):
        return f"{self.get_full_name()} | {self.phone_number}"
