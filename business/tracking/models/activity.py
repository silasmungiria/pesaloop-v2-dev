import uuid
import logging
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

from tracking.utils import ActivityType


logger = logging.getLogger(__name__)
User = get_user_model()

class Activity(models.Model):
    """Tracks user activities with comprehensive request data."""
    
    # Core Metadata
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=ActivityType.choices, default=ActivityType.OTHER)
    flagged = models.BooleanField(default=False)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)

    # User Context
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    session_id = models.CharField(max_length=100, blank=True, null=True)

    # Request Context
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status = models.PositiveSmallIntegerField(null=True, blank=True)
    headers = models.JSONField(default=dict)
    params = models.JSONField(default=dict, blank=True)
    duration = models.FloatField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.CharField(max_length=255, blank=True, null=True)

    # Network Context
    ip_address = models.GenericIPAddressField()
    is_routable = models.BooleanField(default=False)
    is_cloud = models.BooleanField(default=False)
    is_vpn = models.BooleanField(default=False)
    is_tor = models.BooleanField(default=False)

    # Geo Context
    country = models.CharField(max_length=2, blank=True)
    region = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    coordinates = models.CharField(max_length=50, blank=True)

    # ASN Context
    asn = models.CharField(max_length=50, blank=True)
    isp = models.CharField(max_length=100, blank=True)

    # Device Context
    device = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=50, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    is_mobile = models.BooleanField(null=True, blank=True)
    os_version = models.CharField(max_length=50, blank=True)
    browser_version = models.CharField(max_length=50, blank=True)
    is_tablet = models.BooleanField(null=True, blank=True)
    is_pc = models.BooleanField(null=True, blank=True)
    is_bot = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['ip_address', '-timestamp']),
            models.Index(fields=['type', '-timestamp']),
            models.Index(fields=['-timestamp', 'status']),
        ]

    def clean(self):
        """Validate model data before saving."""
        if not self.ip_address:
            raise ValidationError({'ip_address': 'IP address is required'})
        if not self.endpoint:
            raise ValidationError({'endpoint': 'Endpoint is required'})
        if not self.method:
            raise ValidationError({'method': 'HTTP method is required'})
        if not isinstance(self.params, dict):
            self.params = {}

    def __str__(self):
        return f"{self.get_type_display()} @ {self.timestamp}"

    @property
    def location(self):
        """Returns formatted location string."""
        if self.city and self.country:
            return f"{self.city}, {self.country}"
        if self.region and self.country:
            return f"{self.region}, {self.country}"
        return self.country or "Unknown"

    @property
    def device_summary(self):
        """Returns formatted device information."""
        parts = []
        if self.device and self.device != 'Other':
            parts.append(self.device)
        if self.os:
            parts.append(self.os)
        if self.browser:
            parts.append(self.browser)
        return ' / '.join(parts) if parts else 'Unknown device'
