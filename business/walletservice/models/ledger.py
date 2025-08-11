from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import uuid

from .wallet import DigitalWallet
from common import EncryptedFieldsMixin

User = get_user_model()

# ----------------------------------------------------
# LEDGER ENTRY (Immutable, append-only)
# ----------------------------------------------------
class LedgerEntry(EncryptedFieldsMixin, models.Model):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
    ENTRY_TYPE_CHOICES = [
        (DEBIT, "Debit"),
        (CREDIT, "Credit"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    encrypted_wallet = models.ForeignKey(DigitalWallet, on_delete=models.PROTECT, related_name="ledger_entries")
    entry_type = models.CharField(max_length=6, choices=ENTRY_TYPE_CHOICES)
    encrypted_amount = models.DecimalField(max_digits=12, decimal_places=2)
    encrypted_reference = models.CharField(max_length=64, db_index=True)
    encrypted_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Encrypted field names
    encrypted_fields = [
        "wallet",
        "amount",
        "reference",
        "note",
    ]

    class Meta:
        db_table = 'ledger_entries'
        verbose_name = 'Ledger Entry'
        verbose_name_plural = 'Ledger Entries'
        indexes = [
            models.Index(fields=["wallet", "created_at"]),
            models.Index(fields=["reference"]),
        ]
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValueError("Ledger entries are immutable and cannot be updated.")
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.entry_type} {self.amount} for {self.wallet}"


# ----------------------------------------------------
# TRANSACTION (Links both debit & credit entries)
# ----------------------------------------------------
class Transaction(models.Model):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_wallet = models.ForeignKey(DigitalWallet, on_delete=models.CASCADE, related_name="sent_transactions")
    receiver_wallet = models.ForeignKey(DigitalWallet, on_delete=models.CASCADE, related_name="received_transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    @transaction.atomic
    def process(self):
        """
        Executes the transaction by creating debit & credit ledger entries atomically.
        """
        if self.status != self.PENDING:
            raise ValueError("Transaction already processed.")

        # Check sufficient funds
        if self.sender_wallet.balance < self.amount:
            self.status = self.FAILED
            self.save()
            raise ValueError("Insufficient funds.")

        # Create debit entry for sender
        LedgerEntry.objects.create(
            wallet=self.sender_wallet,
            entry_type=LedgerEntry.DEBIT,
            amount=self.amount,
            reference=str(self.id),
            note=f"Transfer to {self.receiver_wallet.user.username}"
        )

        # Create credit entry for receiver
        LedgerEntry.objects.create(
            wallet=self.receiver_wallet,
            entry_type=LedgerEntry.CREDIT,
            amount=self.amount,
            reference=str(self.id),
            note=f"Transfer from {self.sender_wallet.user.username}"
        )

        self.status = self.SUCCESS
        self.completed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"TX[{self.id}] {self.sender_wallet} → {self.receiver_wallet} {self.amount}"
