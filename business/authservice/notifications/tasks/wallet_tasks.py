from celery import shared_task
from ..messages import WalletNotification


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def dispatch_wallet_creation_email_task(self, wallet_id, user_id):
    """Notify user about wallet creation."""
    try:
        return WalletNotification.send_wallet_creation_success(self, wallet_id, user_id)
    except Exception as exc:
        self.retry(exc=exc)
