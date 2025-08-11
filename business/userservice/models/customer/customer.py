# Standard library imports
import uuid

# Third-party library imports
from django.db import models
from django.conf import settings

# Project-specific imports
from data_encryption.services import EncryptionService
from userservice.models import User


class Customer(models.Model):
    def get_default_customer_verified():
        return EncryptionService.encrypt(str(False))

    # Core identification
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='customer_profile', null=False, blank=False)

    # Personal details
    date_of_birth = models.DateField(null=True, blank=True)
    shipping_address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)

    # Document verification
    selfie_image = models.BinaryField(null=True, blank=True)
    is_selfie_image_verified = models.BooleanField(default=False)
    id_image_front = models.BinaryField(null=True, blank=True)
    is_id_image_front_verified = models.BooleanField(default=False)
    id_image_back = models.BinaryField(null=True, blank=True)
    is_id_image_back_verified = models.BooleanField(default=False)
    address_proof_image = models.BinaryField(null=True, blank=True)
    is_address_proof_image_verified = models.BooleanField(default=False)

    # Encrypted personal information
    encrypted_id_type = models.BinaryField(null=True, blank=True)
    encrypted_id_number = models.BinaryField(null=True, blank=True)
    encrypted_country = models.BinaryField(null=True, blank=True)
    encrypted_region_state = models.BinaryField(null=True, blank=True)
    encrypted_city = models.BinaryField(null=True, blank=True)
    encrypted_postal_code = models.BinaryField(null=True, blank=True)
    encrypted_postal_address = models.BinaryField(null=True, blank=True)
    encrypted_residential_address = models.BinaryField(null=True, blank=True)
    encrypted_next_of_kin_name = models.BinaryField(null=True, blank=True)
    encrypted_next_of_kin_relationship = models.BinaryField(null=True, blank=True)
    encrypted_next_of_kin_contact = models.BinaryField(null=True, blank=True)

    # Verification status
    encrypted_verification_status = models.BinaryField(null=True, blank=True)
    encrypted_customer_verified = models.BinaryField(default=get_default_customer_verified)
    encrypted_remarks = models.BinaryField(null=True, blank=True)
    verification_date = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="verified_customer"
    )
    rejection_reason = models.TextField(null=True, blank=True)

    # Version control
    previous_customer = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="next_customer"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Encrypted field names
    _encrypted_fields = [
        'id_type', 'id_number', 'country', 'region_state', 'city',
        'postal_code', 'postal_address', 'residential_address', 'verification_status',
        'remarks', 'customer_verified', 'next_of_kin_name', 'next_of_kin_relationship',
        'next_of_kin_contact'
    ]

    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer Verification'
        verbose_name_plural = 'Customer Verifications'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at', 'user'])]

    def __str__(self):
        return f"Customer {self.user.get_full_name()} - {self.id} ({self.verification_status})"

    # Encryption utilities
    def _get_encrypted_field(self, field_name):
        value = getattr(self, f'encrypted_{field_name}')
        return EncryptionService.decrypt(value) if value else None

    def _set_encrypted_field(self, field_name, value):
        setattr(self, f'encrypted_{field_name}', EncryptionService.encrypt(value))

    # Dynamically create property accessors for encrypted fields
    for field in _encrypted_fields:
        locals()[field] = property(
            lambda self, f=field: self._get_encrypted_field(f),
            lambda self, value, f=field: self._set_encrypted_field(f, value)
        )
