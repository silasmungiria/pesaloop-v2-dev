import uuid
from django.db import models

from userservice.utils import SettlementSchedule
from userservice.models import User


class Merchant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='merchant_profile', null=True, blank=True)
    business_name = models.CharField(max_length=255)
    business_address = models.TextField()
    business_registration_number = models.CharField(max_length=100)
    bank_account_number = models.CharField(max_length=50)
    bank_code = models.CharField(max_length=10)
    settlement_schedule = models.CharField(max_length=20, choices=SettlementSchedule.CHOICES, default=SettlementSchedule.WEEKLY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'merchant'
        verbose_name = 'Merchant'
        verbose_name_plural = 'Merchants'
        ordering = ['business_name']

    def __str__(self):
        return self.business_name
