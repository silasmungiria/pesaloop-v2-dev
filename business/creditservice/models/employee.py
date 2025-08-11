from django.db import models
from django.contrib.auth import get_user_model
from .base import BaseModel
from .employer import Employer
from creditservice.utils import UserVerificationStatus, LOAN_CONFIG

User = get_user_model()

class CreditUser(BaseModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='credit_profile')
    employer = models.ForeignKey(Employer, on_delete=models.PROTECT)
    monthly_salary = models.DecimalField(max_digits=12, decimal_places=2)
    verification_status = models.CharField(
        max_length=20,
        choices=UserVerificationStatus.choices,
        default=UserVerificationStatus.UNVERIFIED
    )
    verified_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='verified_users')
    verified_at = models.DateTimeField(null=True, blank=True)

    @property
    def max_loan_amount(self):
        return self.monthly_salary * LOAN_CONFIG.MAX_SALARY_PERCENTAGE

    @property
    def is_loan_qualified(self):
        return (
            self.verification_status == UserVerificationStatus.VERIFIED and
            self.employer.is_verified
        )

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employer.name})"
