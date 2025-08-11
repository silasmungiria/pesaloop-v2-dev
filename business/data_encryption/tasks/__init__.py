from celery import shared_task
from typing import Dict, Any

from ..services import KeyRotationService
from ..notifications import EncryptionKeyRotationNotifier


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def rotate_encryption_key_task(self) -> Dict[str, Any]:
    """
    Celery task to rotate encryption keys with comprehensive error handling.
    
    Returns:
        dict: Rotation status report
        
    Raises:
        self.retry: When temporary failures occur
        Exception: When unrecoverable errors occur
    """
    try:
        rotation_service = KeyRotationService()
        result = rotation_service.rotate_encryption_key_monthly()
        
        # Return the full rotation report for task result tracking
        return result
        
    except Exception as exc:
        # Only retry on specific recoverable exceptions if needed
        # Here we retry on all exceptions for simplicity
        raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def notify_admin_encryption_key_rotation_task(self, details: Dict[str, Any]) -> bool:
    """
    Celery task to notify admin about key rotation with detailed status.
    
    Args:
        details: Rotation details from the rotation task
        
    Returns:
        bool: True if notification was sent successfully
        
    Raises:
        self.retry: When temporary failures occur
        Exception: When unrecoverable errors occur
    """
    try:
        success = EncryptionKeyRotationNotifier.send_key_rotation_notification(self, details)
        if not success:
            raise ValueError("Notification failed without raising exception")
        return True
        
    except Exception as exc:
        # Implement exponential backoff for retries
        countdown = 60 * (self.request.retries + 1)
        raise self.retry(exc=exc, countdown=countdown)
