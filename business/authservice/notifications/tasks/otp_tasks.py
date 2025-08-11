from celery import shared_task
from ..messages import OTPNotification

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def dispatch_sms_verification_otp_task(self, otp, phone_number):
    """Send SMS OTP notification."""
    try:
        return OTPNotification.send_sms(self, otp, phone_number)
    except Exception as exc:
        self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def dispatch_email_verification_otp_task(self, otp, user_email):
    """Send email OTP notification."""
    try:
        return OTPNotification.send_email(self, otp, user_email)
    except Exception as exc:
        self.retry(exc=exc)
