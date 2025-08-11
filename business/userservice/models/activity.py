# Standard library imports
import uuid

# Third-party library imports
from django.db import models

# Project-specific imports
from .user import User
from common import EncryptedFieldsMixin


class ActivityTrail(EncryptedFieldsMixin, models.Model):
    # Core identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Network information
    ip = models.GenericIPAddressField()
    internet_service_provider = models.CharField(max_length=100, blank=True, null=True)
    
    # Geographic information
    country = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)

    # Request information
    endpoint = models.TextField()
    user_agent = models.TextField()
    request_params = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'activity_trail'
        verbose_name = 'Activity Trail'
        verbose_name_plural = 'Activity Trails'
        indexes = [
            models.Index(fields=['ip', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['endpoint', 'timestamp'])
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user if self.user else 'Anonymous'} - {self.ip} - {self.endpoint} - {self.timestamp}"
