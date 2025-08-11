from .user import (
    UserListAPIView,
    ChangeEmailView,
    ChangePhoneNumberView,
    ChangePasswordView,
    NotificationPreferenceView,
)
from .customer import (
    CustomerFormSubmissionView,
    CustomerImageUploadView,
    CustomerRecordsAdminView,
    CustomerAdminUpdateView,
)
from .merchant import MerchantRegistrationAPIView


__all__ = [
    "UserListAPIView",
    "ChangeEmailView",
    "ChangePhoneNumberView",
    "ChangePasswordView",
    "NotificationPreferenceView",
    "CustomerFormSubmissionView",
    "CustomerImageUploadView",
    "CustomerRecordsAdminView",
    "CustomerAdminUpdateView",
    "MerchantRegistrationAPIView"
]
