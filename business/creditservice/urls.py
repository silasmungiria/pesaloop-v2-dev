from django.urls import path
from .views import (
    LoanRequestAPIView,
    LoanApprovalAPIView,
    LoanDisbursementAPIView,
    LoanRepaymentAPIView,
    UserVerificationAPIView,
    EmployerVerificationAPIView,
    EmployerRegistrationAPIView,
    EmployeeRegistrationAPIView,
    UserLoanHistoryAPIView,
    AdminLoanListAPIView,
    UserProfileAPIView
)

urlpatterns = [
    # Loan endpoints
    path('loans/', LoanRequestAPIView.as_view(), name='loan-request'),
    path('loans/me/', UserLoanHistoryAPIView.as_view(), name='my-loans'),
    path('loans/admin/', AdminLoanListAPIView.as_view(), name='loan-list'),
    path('loans/<uuid:loan_id>/approve/', LoanApprovalAPIView.as_view(), name='loan-approve'),
    path('loans/<uuid:loan_id>/disburse/', LoanDisbursementAPIView.as_view(), name='loan-disburse'),
    path('loans/<uuid:loan_id>/repay/', LoanRepaymentAPIView.as_view(), name='loan-repay'),
    
    # Admin endpoints
    path('admin/loans/', AdminLoanListAPIView.as_view(), name='admin-loans'),
    
    # Verification endpoints
    path('users/verify/', UserVerificationAPIView.as_view(), name='user-verify'),
    path('employers/verify/', EmployerVerificationAPIView.as_view(), name='employer-verify'),
    
    # Registration endpoints
    path('employers/register/', EmployerRegistrationAPIView.as_view(), name='employer-register'),
    path('employees/register/', EmployeeRegistrationAPIView.as_view(), name='employee-register'),
    
    # User endpoints
    path('users/me/', UserProfileAPIView.as_view(), name='user-profile'),
]
