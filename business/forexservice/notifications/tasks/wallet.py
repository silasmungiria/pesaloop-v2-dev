from celery import shared_task
from forexservice.notifications.messages import WalletCreationNotification


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def dispatch_wallet_created_task(self, wallet_id, user_id):
    """Notify user about wallet creation."""
    try:
        return WalletCreationNotification.send(self, wallet_id, user_id)
    except Exception as exc:
        self.retry(exc=exc)
