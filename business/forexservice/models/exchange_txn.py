from django.conf import settings
from django.db import models

from forexservice.utils import ExchangeStatusChoices
from .base import BaseModel


User = settings.AUTH_USER_MODEL


class CurrencyExchangeRecord(BaseModel):
    reference_id = models.CharField(max_length=24, unique=True, editable=False, null=True)
    transaction_type = models.CharField(max_length=50, default='CURRENCY_EXCHANGE')
    status = models.CharField(max_length=50, choices=ExchangeStatusChoices.CHOICES, default=ExchangeStatusChoices.PROCESSING)

    source_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    source_amount = models.DecimalField(max_digits=30, decimal_places=6)
    converted_amount_with_fee = models.DecimalField(max_digits=30, decimal_places=6)

    base_exchange_rate = models.DecimalField(max_digits=30, decimal_places=6)
    platform_exchange_rate = models.DecimalField(max_digits=30, decimal_places=6)

    charged_amount = models.DecimalField(max_digits=30, decimal_places=6)
    charged_amount_currency = models.CharField(max_length=3, null=True)

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='forex_transactions',
        null=True
    )
    payment_provider = models.CharField(max_length=50, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True, help_text="Additional info about the exchange")

    class Meta:
        db_table = 'currency_exchange_records'
        verbose_name = 'Currency Exchange Record'
        verbose_name_plural = 'Currency Exchange Records'
        indexes = [
            models.Index(fields=['user', 'source_currency', 'target_currency']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.source_amount} {self.source_currency} → {self.converted_amount_with_fee} {self.target_currency}"
