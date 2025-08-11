from celery import shared_task
from ..messages import PaymentRequestMessage

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def notify_transaction_request(self, transaction_id):
    """Notify both requester and requestee of a payment request."""
    try:
        PaymentRequestMessage.request(transaction_id, 'requester')
        PaymentRequestMessage.request(transaction_id, 'requestee')
        return

    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def notify_transaction_approval(self, transaction_id):
    """Notify both requester and requestee of payment approval."""
    try:
        PaymentRequestMessage.approval(transaction_id, 'requester')
        PaymentRequestMessage.approval(transaction_id, 'requestee')
        return

    except Exception as exc:
        raise self.retry(exc=exc)



@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def notify_transaction_cancellation(self, transaction_id):
    """Notify both requester and requestee of payment cancellation."""
    try:
        PaymentRequestMessage.cancellation(transaction_id, 'requester')
        PaymentRequestMessage.cancellation(transaction_id, 'requestee')
        return

    except Exception as exc:
        raise self.retry(exc=exc)
