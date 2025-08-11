# models/transaction.py
from django.db import models
from django.conf import settings
from django.utils import timezone

from cardservice.utils import TransactionStatus
from .base import BaseModel
from .card import PaymentCard

class Transaction(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='card_transactions')
    card = models.ForeignKey(PaymentCard, on_delete=models.PROTECT, related_name='transactions')
    transaction_reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in TransactionStatus], default=TransactionStatus.PENDING.value)
    external_reference = models.CharField(max_length=255, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)