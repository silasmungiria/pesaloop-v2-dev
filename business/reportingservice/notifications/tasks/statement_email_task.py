from celery import shared_task
from ..messages import statement_email_messages


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def dispatch_statement_email_notification(self, to_email, subject, body, attachment_file, filename, mimetype):
    """Celery task to send an email statement notification with retries."""
    try:
        statement_email_messages(
            to_email, subject, body, attachment_file, filename, mimetype
        )
    except Exception as exc:
        raise self.retry(exc=exc)
