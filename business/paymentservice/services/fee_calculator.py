from decimal import Decimal, getcontext, Context
import math
from typing import ClassVar

from paymentservice.utils import TransactionFeeConfig


class TransactionFeeCalculator:
    context: ClassVar[Context] = getcontext()
    context.prec = 28

    MAX_PERCENTAGE: ClassVar[Decimal] = TransactionFeeConfig.TRANSACTION_FEE_RATE
    FEE_CAP: ClassVar[Decimal] = TransactionFeeConfig.MAX_TRANSACTION_FEE
    THRESHOLD_AMOUNT: ClassVar[Decimal] = TransactionFeeConfig.FEE_FLAT_THRESHOLD_AMOUNT

    ZERO_AMOUNT: ClassVar[Decimal] = Decimal("0.00")

    @classmethod
    def calculate_transaction_fees(cls, amount: Decimal) -> Decimal:
        if amount < cls.ZERO_AMOUNT:
            raise ValueError("Transaction amount cannot be negative")
        if amount == cls.ZERO_AMOUNT:
            return cls.ZERO_AMOUNT
        if amount >= cls.THRESHOLD_AMOUNT:
            return cls.FEE_CAP

        if not hasattr(cls, '_decay_rate'):
            numerator = float(cls.MAX_PERCENTAGE * cls.THRESHOLD_AMOUNT / cls.FEE_CAP)
            cls._decay_rate = Decimal(math.log(numerator)) / cls.THRESHOLD_AMOUNT

        exponent = -cls._decay_rate * amount
        effective_percentage = cls.MAX_PERCENTAGE * exponent.exp()

        fee = amount * effective_percentage
        return min(fee, cls.FEE_CAP).quantize(Decimal("0.01"))
