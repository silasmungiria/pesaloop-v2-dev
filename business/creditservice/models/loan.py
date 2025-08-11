from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .base import BaseModel
from .employee import CreditUser
from creditservice.utils import LoanStatus, LOAN_CONFIG
from common import ReferenceGenerator

User = get_user_model()

class Loan(BaseModel):
    user = models.ForeignKey(CreditUser, on_delete=models.PROTECT, related_name='loans')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=LoanStatus.choices,
        default=LoanStatus.PENDING
    )
    reference_number = models.CharField(max_length=100, unique=True, default=ReferenceGenerator.loan_reference)
    disbursement_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    interest_accrued = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    processing_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_repayment = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    approved_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.PROTECT, related_name='approved_loans'
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['user']),
            models.Index(fields=['due_date']),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:  # New loan
            if self.amount > self.user.max_loan_amount:
                raise ValueError("Loan amount exceeds maximum allowed")
            self.processing_fee = self.amount * LOAN_CONFIG.PROCESSING_FEE
        super().save(*args, **kwargs)

    @property
    def balance(self):
        if self.status == LoanStatus.REPAID.value:
            return Decimal('0.00')
        total_paid = sum(r.amount_paid for r in self.repayments.all())
        return (self.amount + self.interest_accrued + self.processing_fee) - total_paid

    @property
    def is_overdue(self):
        if self.status != LoanStatus.DISBURSED.value:
            return False
        return timezone.now().date() > self.due_date

    def calculate_interest(self, as_of_date=None):
        from datetime import date
        as_of_date = as_of_date or date.today()
        
        if not self.disbursement_date:
            return Decimal('0.00')
            
        days = (as_of_date - self.disbursement_date).days
        if days <= 0:
            return Decimal('0.00')
            
        self.interest_accrued = self.amount * LOAN_CONFIG.DAILY_INTEREST_RATE * days
        self.save()
        return self.interest_accrued

    def cancel(self):
        if self.status not in [LoanStatus.PENDING.value, LoanStatus.APPROVED.value]:
            raise ValueError("Cannot cancel loan in current state")
        self.status = LoanStatus.CANCELLED.value
        self.save()

    def __str__(self):
        return f"Loan #{self.reference_number} for {self.user.username} - {self.amount}"
