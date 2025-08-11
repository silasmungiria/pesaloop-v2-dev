# authservice/tasks.py

from celery import shared_task
from django.utils import timezone
from authservice.models import OTP

@shared_task
def cleanup_expired_otps():
    """Delete all expired OTPs."""
    now = timezone.now()
    deleted_count, _ = OTP.objects.filter(expires_at__lt=now).delete()
    return f"Deleted {deleted_count} expired OTP(s)."
