from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

from paymentservice.models import TransactionRecord


class PaymentTransactionMessage:
    """Service for sending payment transaction notifications"""

    @classmethod
    def send(cls, transaction_id, recipient_type):
        """
        Notify either payer or payee of a transaction.
        recipient_type: 'payer' or 'payee'
        """
        transaction_record = TransactionRecord.objects.get(id=transaction_id)
        template_name = "payment-transaction.html"

        if recipient_type not in ['payer', 'payee']:
            raise ValueError("recipient_type must be 'payer' or 'payee'")

        is_payer = (recipient_type == 'payer')
        recipient = transaction_record.sender_wallet.wallet_owner if is_payer else transaction_record.receiver_wallet.wallet_owner
        counterparty = transaction_record.receiver_wallet.wallet_owner if is_payer else transaction_record.sender_wallet.wallet_owner

        subject_prefix = "Payment Confirmation - " if is_payer else "Payment Received - "
        subject = f"{subject_prefix}{transaction_record.currency} {"{:,.2f}".format(transaction_record.amount)}"

        reason_message = transaction_record.reason if transaction_record.reason else ""

        html_content = {
            'recipient_name': recipient.get_full_name(),
            'counterparty_name': counterparty.get_full_name(),
            'amount': f"{transaction_record.currency} {"{:,.2f}".format(transaction_record.amount)}",
            'transaction_charge': f"{transaction_record.currency} {"{:,.2f}".format(transaction_record.transaction_charge)}",
            'reference_id': transaction_record.reference_id,
            'reason_message': reason_message,
            'payment_date': timezone.localtime(transaction_record.created_at).strftime("Paid on %B %d, %Y at %H:%M:%S"),
            'is_payer': is_payer,
            'frontend_url': settings.FRONTEND_LOCAL_URL,
            'app_name': settings.APP_NAME,
            'email_support': settings.EMAIL_SUPPORT,
            'copyright_year': settings.COPYRIGHT_YEAR,
            'privacy_policy_url': settings.PRIVACY_POLICY_URL,
            'terms_url': settings.TERMS_URL,
        }

        email_body = render_to_string(template_name, html_content)

        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=settings.EMAIL_FROM_ALERTS,
            to=[recipient.email],
        )
        email.content_subtype = "html"
        email.reply_to = [settings.EMAIL_REPLY_TO]
        email.send()
