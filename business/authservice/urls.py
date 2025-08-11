from django.urls import path
from .views import *

urlpatterns = [
    # User Registration
    path('register/', RegisterUserView.as_view(), name='user-register'),

    # Authservice (Token Management)
    path('token/create/', CreateAuthTokenView.as_view(), name='token-create'),
    path('token/refresh/', RefreshAuthTokenView.as_view(), name='token-refresh'),
    path('token/logout/', LogoutAPIView.as_view(), name='token-logout'),

    # OTP Verification
    path('account/activation/resend/otp/', ResendOTPVerificationView.as_view(), name='otp-resend'),
    path('account/activation/otp/activate/', ActivateAccountWithOTPView.as_view(), name='otp-activate'),

    # Password Management
    path('password/forgot/', ForgotPasswordView.as_view(), name='password-forgot'),
    path('password/reset/', ResetPasswordView.as_view(), name='password-reset'),
]
