from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import get_object_or_404

from userservice import models as user_models
from forexservice import models as exchange_models


class ExchangeSuccessNotification:
    @staticmethod
    def send(exchange_id, user_id):
        """
        Sends an email notification to the user for a successful currency exchange.
        """
        # Fetch user and currency exchange objects
        user = get_object_or_404(user_models.User, id=user_id)
        exchange = get_object_or_404(exchange_models.CurrencyExchangeRecord, id=exchange_id)

        subject = "Currency Exchange Successful"
        template_name = "currency-exchange.html"

        # Ensure numeric values are properly formatted
        def format_currency(amount, currency_code):
            return f"{currency_code} {float(amount):,.2f}" if amount else "N/A"

        context = {
            "user_full_name": user.get_full_name(),
            "exchange": {
                "source_currency": exchange.source_currency,
                "target_currency": exchange.target_currency,
                "source_amount": format_currency(exchange.source_amount, exchange.source_currency),
                "platform_exchange_rate": f"{exchange.platform_exchange_rate:,.6f}",
                "charged_amount": format_currency(exchange.charged_amount, exchange.charged_amount_currency),
                "converted_amt": format_currency(exchange.converted_amount_with_fee, exchange.target_currency),
                "created_at": exchange.created_at,
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
