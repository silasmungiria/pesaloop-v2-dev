from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models

from . import BaseModel
from paymentservice.utils import RequestStatus, RequestAction, TransactionType
from common import ZeroBalanceConfig
from data_encryption.services import EncryptionService

User = get_user_model()


class RequestedTransaction(BaseModel):
    # Core request fields
    reference_id = models.CharField(max_length=24, unique=True, editable=False, null=True)
    transaction_type = models.CharField(max_length=50, choices=TransactionType.CHOICES)
    encrypted_amount = models.BinaryField(default=ZeroBalanceConfig.encrypted_balance)
    currency = models.CharField(max_length=5, default='KES')
    status = models.CharField(max_length=20, choices=RequestStatus.CHOICES, default=RequestStatus.PENDING)
    action = models.CharField(max_length=20, choices=RequestAction.CHOICES, null=True, blank=True)
    
    # User relationships
    requesting_user = models.ForeignKey(User, related_name='p2p_transfer_requests_sent', on_delete=models.PROTECT, null=True)
    requested_user = models.ForeignKey(User, related_name='p2p_transfer_requests_received', on_delete=models.PROTECT, null=True)

    # Tracking information
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    device_fingerprint = models.CharField(max_length=255, blank=True, null=True)
    
    # Additional information
    payment_provider = models.CharField(max_length=50, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'fund_transfer_requests'
        verbose_name = 'Fund Transfer Request'
        verbose_name_plural = 'Fund Transfer Requests'
        indexes = [
            models.Index(fields=['requesting_user', 'requested_user', 'status']),
        ]
        ordering = ['-created_at']

    @property
    def amount(self):
        return Decimal(EncryptionService.decrypt(self.encrypted_amount))
    
    @amount.setter
    def amount(self, value):
        self.encrypted_amount = EncryptionService.encrypt(str(value))

    def __str__(self):
        return f"P2P Transfer Request from {self.requesting_user.email} to {self.requested_user.email} for {self.amount} {self.currency}"
