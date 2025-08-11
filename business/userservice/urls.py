from django.urls import path
from .views import *


urlpatterns = [
    # User Management
    path('list-users/', UserListAPIView.as_view(), name='user-list'),

    # Merchant Registration
    path('merchant/register/', MerchantRegistrationAPIView.as_view(), name='merchant-register'),

    # Security
    path('security/change-email/', ChangeEmailView.as_view(), name='security-change-email'),
    path('security/change-phone-number/', ChangePhoneNumberView.as_view(), name='security-change-phone'),
    path('security/change-password/', ChangePasswordView.as_view(), name='security-change-password'),

    # Preferences
    path('preferences/notification', NotificationPreferenceView.as_view(), name='user-preferences'),

    # Customer Verification
    path('customer/submit/', CustomerFormSubmissionView.as_view(), name='customer-submit'),
    path('customer/upload/<str:image_type>/', CustomerImageUploadView.as_view(), name='customer-upload-image'),

    # Admin views for Customer verification
    path('customer/admin/records/', CustomerRecordsAdminView.as_view(), name='admin-customer-records-list'),
    path('customer/admin/records/<uuid:id>/', CustomerRecordsAdminView.as_view(), name='admin-customer-record-detail'),
    path('customer/admin/records/<uuid:id>/update/', CustomerAdminUpdateView.as_view(), name='admin-customer-record-update'),
]
