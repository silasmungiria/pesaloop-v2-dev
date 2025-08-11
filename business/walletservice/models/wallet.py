import uuid
from decimal import Decimal
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .base import BaseModel
from .currency import Currency
from .ledger import LedgerEntry
from common import ZeroBalanceConfig
from data_encryption.services import EncryptionService

User = get_user_model()


# ----------------------------------------------------
# DIGITAL WALLET (no direct balance storage)
# ----------------------------------------------------
class DigitalWallet(BaseModel):
    wallet_owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='digital_wallets')
    encrypted_balance = models.BinaryField(default=ZeroBalanceConfig.encrypted_balance)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wallet'
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
        unique_together = ('wallet_owner', 'currency')
        indexes = [
            models.Index(fields=['wallet_owner', 'currency', 'is_default', 'is_active']),
        ]
        ordering = ['-created_at']

    # permission_basename = 'wallet'

    # @property
    # def balance(self):
    #     return Decimal(EncryptionService.decrypt(self.encrypted_balance))

    # @balance.setter
    # def balance(self, value):
    #     self.encrypted_balance = EncryptionService.encrypt(str(value))

    def save(self, *args, **kwargs):
        """
        Ensure only one default wallet per currency per user, and deactivate non-default wallets with zero balance
        after 5 days of inactivity.
        """
        if not self.last_updated:
            self.last_updated = timezone.now()

        if self.is_default:
            DigitalWallet.objects.filter(
                wallet_owner=self.wallet_owner,
                currency=self.currency
            ).update(is_default=False)

        if self.balance == 0 and not self.is_default:
            if self.last_updated < timezone.now() - timedelta(days=5):
                self.is_active = False

        if self.balance > 0 and self.is_active:
            self.is_active = True

        super().save(*args, **kwargs)

    @property
    def balance(self) -> Decimal:
        """
        Derived balance calculated from the LedgerEntry table.
        """
        credit_sum = self.ledger_entries.filter(entry_type=LedgerEntry.CREDIT).aggregate(
            total=models.Sum("amount")
        )["total"] or Decimal("0")
        debit_sum = self.ledger_entries.filter(entry_type=LedgerEntry.DEBIT).aggregate(
            total=models.Sum("amount")
        )["total"] or Decimal("0")
        return credit_sum - debit_sum

    def __str__(self):
        return f"Wallet: {self.wallet_owner.email} | Balance: {self.balance} {self.currency.code} | Default: {self.is_default} | Active: {self.is_active}"
