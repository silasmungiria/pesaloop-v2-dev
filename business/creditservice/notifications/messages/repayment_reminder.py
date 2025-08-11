from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from creditservice.models import Repayment


def send_repayment_reminder(repayment_id):
    repayment = Repayment.objects.get(id=repayment_id)
    user = repayment.loan.user.user

    subject = f"Reminder: Upcoming Payment Due for Loan #{repayment.loan.reference_number}"
    context = {
        'user': user,
        'repayment': repayment,
        'app_name': settings.APP_NAME
    }

    html_message = render_to_string('repayment-reminder.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=True
    )
