from datetime import date, timedelta
from decimal import Decimal
from creditservice.models import Repayment
from creditservice.utils import LOAN_CONFIG

class LoanCalculator:
    @staticmethod
    def calculate_repayment(loan, repayment_date=None):
        repayment_date = repayment_date or date.today()
        interest = loan.calculate_interest(repayment_date)
        return {
            'principal': loan.amount,
            'interest': interest,
            'processing_fee': loan.processing_fee,
            'total': loan.amount + interest + loan.processing_fee
        }

    @staticmethod
    def generate_repayment_schedule(loan):
        if not loan.disbursement_date:
            raise ValueError("Loan must be disbursed first")

        due_date = loan.disbursement_date + timedelta(days=LOAN_CONFIG.MAX_LOAN_TERM)
        repayment_amount = LoanCalculator.calculate_repayment(loan, due_date)['total']

        return Repayment.objects.create(
            loan=loan,
            amount_due=repayment_amount,
            due_date=due_date
        )
