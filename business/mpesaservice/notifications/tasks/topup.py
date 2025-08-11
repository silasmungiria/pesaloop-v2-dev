from celery import shared_task
from ..messages import TopUpNotification


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def dispatch_wallet_top_up_initiated(self, reference_id, phone_number):
    """Send wallet top-up initiated notification email."""
    try:
        TopUpNotification.send_initiated_email(reference_id, phone_number)
    except Exception as exc:
        self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def dispatch_wallet_top_up_confirmation(self, reference_id):
    """Send wallet top-up confirmation notification email."""
    try:
        TopUpNotification.send_confirmation_email(reference_id)
    except Exception as exc:
        self.retry(exc=exc)
