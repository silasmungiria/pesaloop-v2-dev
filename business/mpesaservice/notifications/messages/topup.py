from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

from paymentservice.models import TransactionRecord


class BaseNotification:
    """Base class for email notifications with common functionality."""
    
    @staticmethod
    def _get_common_context(transaction):
        """Generate common context data for email templates."""
        return {
            'recipient_name': transaction.receiver_wallet.wallet_owner.get_full_name(),
            'account_balance': f"{transaction.receiver_wallet.currency.code} {'{:,.2f}'.format(transaction.receiver_wallet.balance)}",
            'reference_id': transaction.reference_id,
            'payment_date': timezone.localtime(transaction.created_at).strftime("Paid on %B %d, %Y at %H:%M:%S"),
            'frontend_url': settings.FRONTEND_LOCAL_URL,
            'app_name': settings.APP_NAME,
            'reply_to_email': settings.EMAIL_SUPPORT,
            'copyright_year': settings.COPYRIGHT_YEAR,
            'privacy_policy_url': settings.PRIVACY_POLICY_URL,
            'terms_url': settings.TERMS_URL,
        }

    @staticmethod
    def _send_email(subject, template, context, recipient):
        """Send an HTML email with the given parameters."""
        html_content = render_to_string(template, context)
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.EMAIL_FROM_ALERTS,
            to=[recipient],
        )
        email.content_subtype = "html"
        email.reply_to = [settings.EMAIL_REPLY_TO]
        email.send()


class TopUpNotification(BaseNotification):
    """Handles wallet top-up related email notifications."""

    @staticmethod
    def send_initiated_email(reference_id, phone_number):
        """Notify user that top-up initiation was successful."""
        transaction = TransactionRecord.objects.filter(reference_id=reference_id).first()
        if not transaction:
            return None

        context = BaseNotification._get_common_context(transaction)
        context.update({
            'amount': f"{transaction.receiver_wallet.currency.code} {'{:,.2f}'.format(transaction.amount)}",
            'phone_number': f"+{phone_number}",
        })

        BaseNotification._send_email(
            subject=f"Top-Up of {transaction.receiver_wallet.currency.code} {'{:,.2f}'.format(transaction.amount)} Initiated",
            template='wallet-topup-initiated.html',
            context=context,
            recipient=transaction.receiver_wallet.wallet_owner.email
        )

    @staticmethod
    def send_confirmation_email(reference_id):
        """Notify user of successful top-up completion."""
        transaction = TransactionRecord.objects.filter(reference_id=reference_id).first()
        if not transaction:
            return None

        metadata = transaction.metadata
        callback_metadata_items = (
            metadata.get('Body', {})
            .get('stkCallback', {})
            .get('CallbackMetadata', {})
            .get('Item', [])
        )

        # Extract metadata values
        amount, mpesa_receipt_number, phone_number = None, None, None
        for item in callback_metadata_items:
            if item.get('Name') == 'Amount':
                amount = item.get('Value')
            elif item.get('Name') == 'MpesaReceiptNumber':
                mpesa_receipt_number = item.get('Value')
            elif item.get('Name') == 'PhoneNumber':
                phone_number = item.get('Value')

        context = BaseNotification._get_common_context(transaction)
        context.update({
            'payment_provider': metadata.get('payment_provider', 'M-Pesa'),
            'amount': f"{transaction.receiver_wallet.currency.code} {'{:,.2f}'.format(amount)}" if amount else 'N/A',
            'mpesa_receipt_number': mpesa_receipt_number or 'N/A',
            'phone_number': f"+{phone_number}" if phone_number else 'N/A',
            'reason_message': metadata.get('reason', ''),
        })

        BaseNotification._send_email(
            subject="Wallet Top-Up Confirmation",
            template='wallet-topup.html',
            context=context,
            recipient=transaction.receiver_wallet.wallet_owner.email
        )
