from celery import shared_task
from forexservice.notifications.messages import ExchangeSuccessNotification


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def dispatch_exchange_success_task(self, exchange_id, user_id):
    """Notify user about currency exchange."""
    try:
        return ExchangeSuccessNotification.send(self, exchange_id, user_id)
    except Exception as exc:
        self.retry(exc=exc)
