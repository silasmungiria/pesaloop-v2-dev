from decimal import Decimal
from django.db import models

from . import BaseModel, RequestedTransaction
from common import DefaultConfig, EncryptedFieldsMixin
from paymentservice.utils import TransactionType, TransactionStatus


class TransactionRecord(BaseModel, EncryptedFieldsMixin):
    # Core transaction fields
    reference_id = models.CharField(max_length=36, unique=True, editable=False, null=True)
    transaction_type = models.CharField(max_length=50, choices=TransactionType.CHOICES)
    encrypted_amount = models.BinaryField(default=DefaultConfig.balance)
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

    # Encrypted fields
    encrypted_fields = [
        'amount',
        # 'currency',
        # 'transaction_charge',
        # 'reason',
    ]

    class Meta:
        db_table = 'fund_transaction_records'
        verbose_name = 'Fund Transaction Record'
        verbose_name_plural = 'Fund Transaction Records'
        indexes = [
            models.Index(fields=['sender_wallet', 'receiver_wallet', 'status']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"Transaction {self.id} | Status: {self.status}"
    
    
    # @transaction.atomic
    # def process(self):
    #     """
    #     Executes the transaction by creating debit & credit ledger entries atomically.
    #     """
    #     if self.status != self.PENDING:
    #         raise ValueError("Transaction already processed.")

    #     # Check sufficient funds
    #     if self.sender_wallet.balance < self.amount:
    #         self.status = self.FAILED
    #         self.save()
    #         raise ValueError("Insufficient funds.")

    #     # Create debit entry for sender
    #     LedgerEntry.objects.create(
    #         wallet=self.sender_wallet,
    #         entry_type=LedgerEntry.DEBIT,
    #         amount=self.amount,
    #         reference=str(self.id),
    #         note=f"Transfer to {self.receiver_wallet.user.username}"
    #     )

    #     # Create credit entry for receiver
    #     LedgerEntry.objects.create(
    #         wallet=self.receiver_wallet,
    #         entry_type=LedgerEntry.CREDIT,
    #         amount=self.amount,
    #         reference=str(self.id),
    #         note=f"Transfer from {self.sender_wallet.user.username}"
    #     )

    #     self.status = self.SUCCESS
    #     self.completed_at = timezone.now()
    #     self.save()
