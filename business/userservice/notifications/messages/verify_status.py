# Third-party library imports
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class CustomerVerificationEmail:

    @staticmethod
    def send(self, customer_record_id, verification_status):
        """Send email notification for customer record in review."""
        # Local import to break circular dependency
        from userservice.models import Customer
        
        customer_record = Customer.objects.select_for_update().get(id=customer_record_id)
        verification_status = verification_status.replace('_', ' ').title()

        subject = f"Customer Verification {verification_status}"
        template_name = "customer-verification-status.html"

        html_content = {
            'customer_record': customer_record,
            'verification_status': verification_status,
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
            to=[customer_record.user.email],
        )
        email.content_subtype = "html"
        email.reply_to = [settings.EMAIL_REPLY_TO]
        email.send()
