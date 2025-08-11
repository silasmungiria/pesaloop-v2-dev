import logging
from datetime import timedelta
from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from paymentservice.models import RequestedTransaction


logger = logging.getLogger(__name__)
PAYMENT_REMINDER_DAYS = 2  # Days after which to send reminders

class PaymentReminderService:
    """Service for handling bulk payment reminder emails"""

    @classmethod
    def send_reminders(cls, batch_size=100):
        """
        Send payment reminder emails in bulk
        Args:
            batch_size (int): Maximum number of reminders to send in this batch
        Returns:
            tuple: (success_count, failure_count)
        """
        if not all([settings.EMAIL_FROM_ALERTS, settings.EMAIL_REPLY_TO]):
            logger.error("Email settings not configured")
            return (0, 0)

        reminder_cutoff = timezone.now() - timedelta(days=PAYMENT_REMINDER_DAYS or 5)
        
        try:
            pending_requests = (
                RequestedTransaction.objects
                .filter(
                    status='pending',
                    created_at__lt=reminder_cutoff,
                    requested_user__is_active=True
                )
                .select_related('requesting_user', 'requested_user')
                .order_by('created_at')[:batch_size]
            )
            
            if not pending_requests:
                logger.debug("No pending payment requests found")
                return (0, 0)

            messages = cls._prepare_messages(pending_requests)
            return cls._send_bulk_emails(messages)

        except Exception as e:
            logger.exception("Failed to process payment reminders")
            return (0, len(pending_requests) if 'pending_requests' in locals() else 0)

    @classmethod
    def _prepare_messages(cls, requests):
        """Prepare email messages for bulk sending"""
        messages = []
        template_name = "payment-reminder.html"
        
        for request in requests:
            try:
                html_content = {
                    'requester_name': request.requesting_user.get_full_name(),
                    'requestee_name': request.requested_user.get_full_name(),
                    'amount': f"{request.currency} {request.amount:,.2f}",
                    'reminder_message': (
                        f"Your payment request of {request.currency} {request.amount:,.2f} "
                        "is still pending."
                    ),
                    'payment_date': timezone.localtime(request.created_at).strftime("%B %d, %Y at %H:%M:%S"),
                    'frontend_url': settings.FRONTEND_LOCAL_URL,
                    'app_name': settings.APP_NAME,
                    'email_support': settings.EMAIL_SUPPORT,
                    'copyright_year': settings.COPYRIGHT_YEAR,
                    'privacy_policy_url': settings.PRIVACY_POLICY_URL,
                    'terms_url': settings.TERMS_URL,
                }

                email_body = render_to_string(template_name, html_content)

                message = EmailMultiAlternatives(
                    subject=f"Payment Request Reminder - {request.currency} {request.amount:,.2f}",
                    body=email_body,  # Text fallback
                    from_email=settings.EMAIL_FROM_ALERTS,
                    to=[request.requested_user.email],
                    reply_to=[settings.EMAIL_REPLY_TO],
                )
                message.attach_alternative(email_body, "text/html")
                messages.append(message)
                
            except Exception as e:
                logger.error(f"Failed to prepare reminder for request {request.id}: {str(e)}")
                continue
                
        return messages

    @classmethod
    def _send_bulk_emails(cls, messages):
        """Send prepared messages in bulk"""
        if not messages:
            return (0, 0)

        success_count = 0
        try:
            with get_connection(
                fail_silently=False,
                timeout=settings.EMAIL_TIMEOUT or 10
            ) as connection:
                results = connection.send_messages(messages)
                success_count = len([r for r in results if r == 1])
                
        except Exception as e:
            logger.error(f"Bulk email send failed: {str(e)}")
            
        failure_count = len(messages) - success_count
        if failure_count > 0:
            logger.warning(f"Failed to send {failure_count} reminders")
            
        return (success_count, failure_count)
