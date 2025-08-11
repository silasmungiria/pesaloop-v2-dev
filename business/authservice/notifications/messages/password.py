# Third-party library imports
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode

# Project-specific imports
from userservice.models import User


token_generator = PasswordResetTokenGenerator()

class PasswordNotification:
    @staticmethod
    def send_reset_link(self, user_id):
        """Send password reset email."""
        user = User.objects.get(id=user_id)
        uid = urlsafe_base64_encode(force_str(user.pk).encode())
        token = token_generator.make_token(user)
        reset_url = f"{settings.FRONTEND_LOCAL_URL}/auth/reset-password?uid={uid}&token={token}"
        template_name = "password-reset-request.html"
        
        subject = f"Reset Your Password"
        html_content = {
            'user_full_name': user.get_full_name(),
            'reset_url': reset_url,
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
            to=[user.email],
        )
        email.content_subtype = "html"
        email.reply_to = [settings.EMAIL_REPLY_TO]
        email.send()


    @staticmethod
    def send_reset_success(self, user_id):
        """Notify user of successful password reset."""
        user = User.objects.get(id=user_id)
        template_name = "password-reset-success.html"

        subject = f"Password Reset Successful"
        html_content = {
            "user_full_name": user.get_full_name(),
            "support_url": settings.FRONTEND_LOCAL_URL + '/support',
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
        email.send()
