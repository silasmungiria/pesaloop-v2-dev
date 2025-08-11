from django.db import models
from django.utils import timezone
from .base import BaseModel
from .loan import Loan
from creditservice.utils import RepaymentStatus

class Repayment(BaseModel):
    loan = models.ForeignKey(Loan, on_delete=models.PROTECT, related_name='repayments')
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=RepaymentStatus.choices,
        default=RepaymentStatus.PENDING
    )
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['due_date']
        verbose_name = "Loan Repayment"
        verbose_name_plural = "Loan Repayments"

    def save(self, *args, **kwargs):
        # Auto-update status based on payment
        if self.amount_paid >= self.amount_due:
            self.status = RepaymentStatus.PAID
        elif self.amount_paid > 0:
            self.status = RepaymentStatus.PARTIAL
        elif self.due_date and self.due_date < timezone.now().date():
            self.status = RepaymentStatus.OVERDUE
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Repayment #{self.id} for Loan {self.loan.id}"
