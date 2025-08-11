from celery import shared_task
from ..messages import PasswordNotification


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def dispatch_password_reset_email_task(self, user_id):
    """Notify user about password reset request."""
    try:
        return PasswordNotification.send_reset_link(self, user_id)
    except Exception as exc:
        self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def dispatch_password_reset_confirmation_email_task(self, user_id):
    """Notify user about successful password reset."""
    try:
        return PasswordNotification.send_reset_success(self, user_id)
    except Exception as exc:
        self.retry(exc=exc)
