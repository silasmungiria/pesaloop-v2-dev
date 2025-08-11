from django.conf import settings
from django.core.mail import EmailMessage
from typing import Optional, List


class EncryptionKeyRotationNotifier:
    """
    Handles notifications related to encryption key rotation events.
    """

    @staticmethod
    def _get_admin_emails() -> List[str]:
        """
        Retrieves admin emails from settings with validation.
        Returns a list of email addresses.
        """
        emails = []

        email_security = getattr(settings, "EMAIL_SECURITY", None)
        if email_security:
            emails.append(email_security)

        email_sys_admin = getattr(settings, "EMAIL_SYS_ADMIN", None)
        if email_sys_admin:
            emails.append(email_sys_admin)

        if not emails:
            raise ValueError("No admin emails configured in settings (EMAIL_SECURITY or EMAIL_SYS_ADMIN)")

        return emails

    @staticmethod
    def _get_sender_email() -> str:
        """Retrieves sender email from settings with validation."""
        sender_email = getattr(settings, "EMAIL_FROM_ALERTS", None)
        if not sender_email:
            raise ValueError("EMAIL_FROM_ALERTS not configured in settings")
        return sender_email

    @staticmethod
    def _get_reply_to_email() -> Optional[str]:
        """Retrieves reply-to email from settings."""
        return getattr(settings, "EMAIL_REPLY_TO", None)

    @classmethod
    def send_key_rotation_notification(cls, details: dict = None) -> bool:
        """
        Sends notification about successful key rotation.

        Args:
            details: Additional rotation details to include in notification

        Returns:
            bool: True if email was sent successfully

        Raises:
            ValueError: If required email settings are not configured
        """
        try:
            subject = "🔐 System Notification: Encryption Key Rotation Completed"

            message = (
                "System Notification:\n\n"
                "The encryption key rotation has been successfully completed.\n"
                "All sensitive data has been re-encrypted with the new key.\n\n"
            )

            if details:
                message += (
                    f"Rotation Details:\n"
                    f"- Timestamp: {details.get('timestamp')}\n"
                    f"- Models Processed: {details.get('models_processed', 0)}\n"
                    f"- Records Processed: {details.get('records_processed', 0)}\n"
                    f"- Failed Records: {details.get('failed_records', 0)}\n\n"
                )

            message += "No further action is required."

            email = EmailMessage(
                subject=subject,
                body=message,
                to=cls._get_admin_emails(),
                from_email=cls._get_sender_email(),
                reply_to=[cls._get_reply_to_email()] if cls._get_reply_to_email() else None
            )
            email.content_subtype = "plain"
            email.send()
            return True

        except Exception as e:
            raise ValueError(f"Failed to send notification: {str(e)}") from e
