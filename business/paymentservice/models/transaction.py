from decimal import Decimal
from django.db import models

from . import BaseModel, RequestedTransaction
from paymentservice.utils import TransactionType, TransactionStatus
from common import ZeroBalanceConfig
from data_encryption.services import EncryptionService


class TransactionRecord(BaseModel):
    # Core transaction fields
    reference_id = models.CharField(max_length=36, unique=True, editable=False, null=True)
    transaction_type = models.CharField(max_length=50, choices=TransactionType.CHOICES)
    encrypted_amount = models.BinaryField(default=ZeroBalanceConfig.encrypted_balance)
    currency = models.CharField(max_length=5, default='KES')
    transaction_charge = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=TransactionStatus.CHOICES, default=TransactionStatus.PENDING)
    fraud_checked = models.BooleanField(default=False)

    # Relationship fields
    sender_wallet = models.ForeignKey('walletservice.DigitalWallet', on_delete=models.PROTECT, related_name='sent_transactions', null=True)
    receiver_wallet = models.ForeignKey('walletservice.DigitalWallet', on_delete=models.PROTECT, related_name='received_transactions', null=True)
    request_record = models.ForeignKey(RequestedTransaction, on_delete=models.PROTECT, null=True, blank=True)
    
    # Provider information
    payment_provider = models.CharField(max_length=50, null=True, blank=True)
    
    # Tracking information
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    device_fingerprint = models.CharField(max_length=255, blank=True, null=True)
    
    # Additional information
    reason = models.TextField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'fund_transaction_records'
        verbose_name = 'Fund Transaction Record'
        verbose_name_plural = 'Fund Transaction Records'
        indexes = [
            models.Index(fields=['sender_wallet', 'receiver_wallet', 'status']),
        ]
        ordering = ['-created_at']

    @property
    def amount(self):
        return Decimal(EncryptionService.decrypt(self.encrypted_amount))
    
    @amount.setter
    def amount(self, value):
        self.encrypted_amount = EncryptionService.encrypt(str(value))

    def __str__(self):
        return f"Transaction {self.id} | Status: {self.status}"
