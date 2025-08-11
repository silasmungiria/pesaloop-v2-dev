from celery import shared_task
import logging
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from creditservice.models import Loan, Repayment
from creditservice.utils import LoanStatus, RepaymentStatus
from creditservice.services import LoanCalculator
from creditservice.notifications.messages import (
    send_loan_approved_notification,
    send_repayment_reminder
)

logger = logging.getLogger(__name__)

@shared_task
def accrue_daily_interest():
    """Task to calculate daily interest for all active loans"""
    active_loans = Loan.objects.filter(
        status=LoanStatus.DISBURSED.value,
        disbursement_date__isnull=False
    )

    for loan in active_loans:
        try:
            previous_interest = loan.interest_accrued
            loan.calculate_interest()
            
            # Only notify if significant interest accrued (>1% of principal)
            if (loan.interest_accrued - previous_interest) >= (loan.amount * Decimal('0.01')):
                send_loan_approved_notification.delay(loan.id)
                
        except Exception as e:
            logger.error(f"Error processing interest for loan {loan.id}: {str(e)}")
            continue

@shared_task
def flag_overdue_repayments():
    """Task to flag overdue repayments and send reminders"""
    overdue_repayments = Repayment.objects.filter(
        status=RepaymentStatus.PENDING.value,
        due_date__lt=timezone.now().date()
    )

    for repayment in overdue_repayments:
        try:
            repayment.status = RepaymentStatus.OVERDUE.value
            repayment.save()
            send_repayment_reminder.delay(repayment.id)
        except Exception as e:
            logger.error(f"Error processing repayment {repayment.id}: {str(e)}")
            continue

@shared_task
def disburse_approved_loans_hourly():
    """Task to automatically disburse approved loans after verification"""
    approved_loans = Loan.objects.filter(
        status=LoanStatus.APPROVED.value,
        approved_at__isnull=False
    )

    for loan in approved_loans:
        try:
            # Only disburse if approved more than 1 hour ago
            if timezone.now() - loan.approved_at > timedelta(hours=1):
                loan.status = LoanStatus.DISBURSED.value
                loan.disbursement_date = timezone.now().date()
                loan.due_date = loan.disbursement_date + timedelta(days=30)
                loan.save()
                LoanCalculator.generate_repayment_schedule(loan)
                send_loan_approved_notification.delay(loan.id)
        except Exception as e:
            logger.error(f"Error disbursing loan {loan.id}: {str(e)}")
            continue
