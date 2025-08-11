from django.conf import settings
from django.core.mail import EmailMessage


def statement_email_messages(to_email, subject, body, attachment_file, filename, mimetype):
    """Compose and send an email with an attachment."""
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_FROM_ALERTS,
        to=[to_email],
    )
    email.attach(filename, attachment_file, mimetype)
    email.send(fail_silently=False)
