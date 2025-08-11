from enum import Enum

class TransactionStatus(Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'


class CardType(Enum):
    VISA = 'VISA'
    MASTERCARD = 'MASTERCARD'
    AMEX = 'AMEX'
    OTHER = 'OTHER'