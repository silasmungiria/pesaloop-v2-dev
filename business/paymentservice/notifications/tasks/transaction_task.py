from celery import shared_task
from ..messages import PaymentTransactionMessage


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def notify_transaction_completion(self, transaction_id):
    """Notify sender and receiver of transaction."""
    try:
        PaymentTransactionMessage.send(transaction_id, 'payer')
        PaymentTransactionMessage.send(transaction_id, 'payee')
        return

    except Exception as exc:
        raise self.retry(exc=exc)
