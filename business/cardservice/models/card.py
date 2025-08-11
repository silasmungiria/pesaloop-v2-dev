# models/card.py
from django.db import models
from django.conf import settings

from cardservice.utils import CardType
from .base import BaseModel

class PaymentCard(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_cards')
    card_token = models.CharField(max_length=255, unique=True)
    last_four = models.CharField(max_length=4)
    card_type = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in CardType])
    expiry_month = models.IntegerField()
    expiry_year = models.IntegerField()
    is_active = models.BooleanField(default=True)