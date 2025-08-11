from decimal import Decimal


class LOAN_CONFIG:
    MAX_SALARY_PERCENTAGE = Decimal('0.8')  # 80% of salary
    DAILY_INTEREST_RATE = Decimal('0.0005')  # Approx 1.5% monthly
    PROCESSING_FEE = Decimal('0.01')         # 1% processing fee
    MIN_LOAN_AMOUNT = Decimal('500.00')      # Minimum loan amount
    MAX_LOAN_TERM = 30                        # Max days (1 month)

    @staticmethod
    def get_config():
        return {
            'MAX_SALARY_PERCENTAGE': LOAN_CONFIG.MAX_SALARY_PERCENTAGE,
            'DAILY_INTEREST_RATE': LOAN_CONFIG.DAILY_INTEREST_RATE,
            'PROCESSING_FEE': LOAN_CONFIG.PROCESSING_FEE,
            'MIN_LOAN_AMOUNT': LOAN_CONFIG.MIN_LOAN_AMOUNT,
            'MAX_LOAN_TERM': LOAN_CONFIG.MAX_LOAN_TERM,
        }
