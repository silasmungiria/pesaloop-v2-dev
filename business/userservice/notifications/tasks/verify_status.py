from celery import shared_task
from ..messages import CustomerVerificationEmail

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_verification_email(self, customer_record_id, verification_status):
    """Sends a verification status email to the customer."""
    try:
        return CustomerVerificationEmail.send(self, customer_record_id, verification_status)
    except Exception as exc:
        self.retry(exc=exc)
