from reportingservice.utils import APP_NAME, STATEMENT_PERIOD_DAYS
from reportingservice.notifications import dispatch_statement_email_notification


def create_email_subject_and_message(user, filename):
    base_filename = filename.rsplit('.', 1)[0]
    subject = f"Transaction Statement: {base_filename} - Last {STATEMENT_PERIOD_DAYS} Days"
    message = (
        f"Dear {user.get_full_name()},\n\n"
        f"Please find attached your transaction report for the last {STATEMENT_PERIOD_DAYS} days.\n\n"
        "If you have any questions or need assistance, feel free to contact our support team.\n\n"
        f"Best regards,\n{APP_NAME} Support Team"
    )
    return subject, message


def send_email_with_attachment(to_email, subject, body, attachment, filename, mimetype):
    dispatch_statement_email_notification.delay(
        to_email=to_email,
        subject=subject,
        body=body,
        attachment_file=attachment,
        filename=filename,
        mimetype=mimetype
    )
