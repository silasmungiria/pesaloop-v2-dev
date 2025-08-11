# Third-party library imports
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from twilio.rest import Client

# Project-specific imports
from userservice.models import User
from authservice.utils import OTP_EXPIRATION_MINUTES


class OTPNotification:
    @staticmethod
    def send_sms(self, otp, phone_number):
        """Send OTP via SMS."""
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_=settings.TWILIO_SMS_FROM,
            body=f"Your OTP is {otp}. It will expire in {OTP_EXPIRATION_MINUTES} minutes.",
            to=f"{phone_number}"
        )
        return message.sid


    @staticmethod
    def send_email(self, otp, user_email):
        """Send OTP via email."""
        subject = f"Your Verification Code - {otp}"
        user_full_name = User.objects.get(email=user_email).get_full_name()
        template_name = "otp.html"
        
        html_content = {
            'otp': otp,
            'expires_in_minutes': OTP_EXPIRATION_MINUTES,
            'user_full_name': user_full_name,
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
            to=[user_email],
        )
        email.content_subtype = "html"
        email.reply_to = [settings.EMAIL_REPLY_TO]
        email.send()
