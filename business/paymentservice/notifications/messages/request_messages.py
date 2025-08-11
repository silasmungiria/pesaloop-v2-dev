from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

from paymentservice.models import RequestedTransaction, TransactionRecord



class PaymentRequestMessage:
    """Service for sending payment request notifications"""
    
    @classmethod
    def request(cls, transaction_id, recipient_type):
        """
        Notify either requester or requestee of a payment request.
        recipient_type: 'requester' or 'requestee'
        """
        payment_request = RequestedTransaction.objects.get(id=transaction_id)
        template_name = "payment-request.html"

        if recipient_type not in ['requester', 'requestee']:
            raise ValueError("recipient_type must be 'requester' or 'requestee'")

        is_requester = (recipient_type == 'requester')
        recipient = payment_request.requesting_user if is_requester else payment_request.requested_user
        counterparty = payment_request.requested_user if is_requester else payment_request.requesting_user

        subject_prefix = "Payment Request Sent - " if is_requester else "Payment Request Received - "
        subject = f"{subject_prefix}{payment_request.currency} {"{:,.2f}".format(payment_request.amount)}"

        reason_message = payment_request.reason if payment_request.reason else ""

        html_content = {
            'recipient_name': recipient.get_full_name(),
            'counterparty_name': counterparty.get_full_name(),
            'amount': f"{payment_request.currency} {"{:,.2f}".format(payment_request.amount)}",
            'reason_message': reason_message,
            'request_id': payment_request.reference_id,
            'date': timezone.localtime(payment_request.created_at).strftime("Sent on %B %d, %Y at %H:%M:%S"),
            'is_requester': is_requester,
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
            to=[recipient.email]
        )
        email.content_subtype = "html"
        email.reply_to = [settings.EMAIL_REPLY_TO]
        email.send()

    @classmethod
    def approval(cls, transaction_id, recipient_type):
        """
        Notify either requester or requestee of payment request approval.
        recipient_type: 'requester' or 'requestee'
        """
        transaction = TransactionRecord.objects.get(id=transaction_id)
        template_name = "payment-approval.html"

        if recipient_type not in ['requester', 'requestee']:
            raise ValueError("recipient_type must be 'requester' or 'requestee'")

        is_requester = (recipient_type == 'requester')
        recipient = transaction.sender_wallet.wallet_owner if is_requester else transaction.receiver_wallet.wallet_owner
        counterparty = transaction.receiver_wallet.wallet_owner if is_requester else transaction.sender_wallet.wallet_owner

        subject = (
            f"Payment Request Approval Confirmed - {transaction.reference_id}"
            if is_requester else
            f"Payment Request Approved - {transaction.reference_id}"
        )

        approval_message = (
            f"Your payment request of {"{:,.2f}".format(transaction.amount)} has been approved."
            if is_requester else
            f"Your approval of the payment request of {"{:,.2f}".format(transaction.amount)} has been confirmed."
        )

        html_content = {
            'recipient_name': recipient.get_full_name(),
            'counterparty_name': counterparty.get_full_name(),
            'amount': f"{transaction.sender_wallet.currency} {"{:,.2f}".format(transaction.amount)}",
            'reference_id': transaction.reference_id,
            'approval_message': approval_message,
            'payment_date': timezone.localtime(transaction.created_at).strftime("Approved on %B %d, %Y at %H:%M:%S"),
            'is_requester': is_requester,
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

    @classmethod
    def cancellation(cls, transaction_id, recipient_type):
        """
        Notify either requester or requestee of payment request cancellation.
        recipient_type: 'requester' or 'requestee'
        """
        transfer_request = RequestedTransaction.objects.get(id=transaction_id)
        template_name = "payment-cancelled.html"

        if recipient_type not in ['requester', 'requestee']:
            raise ValueError("recipient_type must be 'requester' or 'requestee'")

        is_requester = (recipient_type == 'requester')
        recipient = transfer_request.requesting_user if is_requester else transfer_request.requested_user
        counterparty = transfer_request.requested_user if is_requester else transfer_request.requesting_user

        subject = f"Payment Request Cancelled - {transfer_request.currency} {"{:,.2f}".format(transfer_request.amount)}"

        cancellation_message = (
            f"Your payment request of {transfer_request.currency} {"{:,.2f}".format(transfer_request.amount)} has been cancelled."
            if is_requester else
            f"Your approval of the payment request of {transfer_request.currency} {"{:,.2f}".format(transfer_request.amount)} has been cancelled."
        )

        html_content = {
            'recipient_name': recipient.get_full_name(),
            'counterparty_name': counterparty.get_full_name(),
            'amount': f"{transfer_request.currency} {"{:,.2f}".format(transfer_request.amount)}",
            'reference_id': transfer_request.reference_id,
            'cancellation_message': cancellation_message,
            'payment_date': timezone.localtime(transfer_request.created_at).strftime("Cancelled on %B %d, %Y at %H:%M:%S"),
            'is_requester': is_requester,
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
