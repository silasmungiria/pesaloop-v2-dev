from datetime import date
from decimal import Decimal
from creditservice.models import Loan, Repayment
from creditservice.utils import LoanStatus, RepaymentStatus
from .calculation import LoanCalculator

class ReconciliationService:
    @staticmethod
    def process_repayment(loan, amount=None):
        repayment_details = LoanCalculator.calculate_repayment(loan)
        amount_paid = amount or repayment_details['total']

        repayment = Repayment.objects.create(
            loan=loan,
            amount_due=repayment_details['total'],
            amount_paid=amount_paid,
            payment_date=date.today(),
            status=RepaymentStatus.PAID if amount_paid >= repayment_details['total'] else RepaymentStatus.PARTIAL
        )

        if amount_paid >= repayment_details['total']:
            loan.status = LoanStatus.REPAID
        loan.total_repayment = amount_paid
        loan.save()

        return repayment

    @staticmethod
    def reconcile_employer_loans(employer_id):
        loans = Loan.objects.filter(
            user__employer_id=employer_id,
            status=LoanStatus.DISBURSED.value
        )

        for loan in loans:
            ReconciliationService.process_repayment(loan)
