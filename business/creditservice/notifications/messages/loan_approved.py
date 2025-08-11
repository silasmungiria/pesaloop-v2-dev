from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from creditservice.models import Loan


def send_loan_approved_notification(loan_id):
    loan = Loan.objects.get(id=loan_id)
    user = loan.user.user

    subject = f"Your Loan #{loan.reference_number} Has Been Approved"
    context = {
        'user': user,
        'loan': loan,
        'app_name': settings.APP_NAME
    }

    html_message = render_to_string('loan-approved.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=True
    )
