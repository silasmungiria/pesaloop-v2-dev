# Third-party library imports
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

# Project-specific imports
from walletservice.models import DigitalWallet
from userservice.models import User


token_generator = PasswordResetTokenGenerator()

class WalletNotification:
    @staticmethod
    def send_wallet_creation_success(self, wallet_id, user_id):
        """
        Sends an email notification to the user when their wallet is created.
        """
        user = get_object_or_404(User, id=user_id)
        wallet = get_object_or_404(DigitalWallet, id=wallet_id)

        subject = f"Your {settings.APP_NAME} Wallet is Ready"
        template_name = "wallet-created.html"

        html_content = {
            "user_full_name": user.get_full_name(),
            "wallet": {
                "balance": f"{wallet.currency.code} {"{:,.2f}".format(wallet.balance)}",
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
        email_body = render_to_string(template_name, html_content)
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=settings.EMAIL_FROM_ALERTS,
            to=[user.email],
        )
        email.content_subtype = "html"
        email.reply_to = [settings.EMAIL_REPLY_TO]
        email.send(fail_silently=False)
