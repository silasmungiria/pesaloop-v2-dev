from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import get_object_or_404

from userservice import models as user_models
from walletservice import models as wallet_models


class WalletCreationNotification:
    @staticmethod
    def send(wallet_id, user_id):
        """
        Sends an email notification to the user when a new wallet is created for an existing user.
        """
        user = get_object_or_404(user_models.User, id=user_id)
        wallet = get_object_or_404(wallet_models.DigitalWallet, id=wallet_id)

        subject = f"New Wallet Created for You on {settings.APP_NAME}"
        template_name = "wallet-created-forex.html"

        context = {
            "user_full_name": user.get_full_name(),
            "wallet": {
                "balance": f"{wallet.currency.code} {'{:,.2f}'.format(wallet.balance)}",
                "currency": wallet.currency.code,
                "is_default": wallet.is_default,
                "last_updated": wallet.last_updated,
            },
            "app_name": settings.APP_NAME,
            'email_support': settings.EMAIL_SUPPORT,
            'copyright_year': settings.COPYRIGHT_YEAR,
            'privacy_policy_url': settings.PRIVACY_POLICY_URL,
            'terms_url': settings.TERMS_URL,
        }

        # Render the email content
        email_body = render_to_string(template_name, context)

        # Send the email
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=settings.EMAIL_FROM_ALERTS,
            to=[user.email],
        )
        email.content_subtype = "html"
        email.reply_to = [settings.EMAIL_REPLY_TO]
        email.send(fail_silently=False)
