from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from ..messages import PaymentReminderService

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    soft_time_limit=300,
    time_limit=330
)
def send_queued_transaction_reminders(self, batch_size=None):
    """
    Celery task for dispatching payment reminders in batches
    Args:
        batch_size (int): Number of reminders per batch (default from settings)
    """
    batch_size = batch_size or getattr(settings, 'EMAIL_BATCH_SIZE', 100)
    
    try:
        success, failures = PaymentReminderService.send_reminders(batch_size)
        
        logger.info(
            f"Reminder batch completed - Success: {success}, Failures: {failures}",
            extra={
                'success_count': success,
                'failure_count': failures
            }
        )
        
        # If we processed a full batch, queue next one
        if success >= batch_size:
            self.apply_async(
                kwargs={'batch_size': batch_size},
                countdown=settings.EMAIL_BATCH_DELAY or 30
            )
            
        return {
            'success': success,
            'failures': failures,
            'batch_size': batch_size
        }
        
    except Exception as exc:
        logger.exception("Payment reminder task failed")
        self.retry(
            exc=exc,
            countdown=min(300, self.default_retry_delay * (self.request.retries + 1))
        )
