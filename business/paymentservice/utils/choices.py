# choices.py

class RequestStatus:
    PENDING = 'PENDING'
    CANCELLED = 'CANCELLED'
    SUCCESS = 'SUCCESS'
    DECLINED = 'DECLINED'

    CHOICES = [
        (PENDING, 'Pending'),
        (CANCELLED, 'Cancelled'),
        (SUCCESS, 'Success'),
        (DECLINED, 'Declined'),
    ]


class RequestAction:
    APPROVE = 'APPROVE'
    CANCEL = 'CANCEL'
    DECLINE = 'DECLINE'

    CHOICES = [
        (APPROVE, 'Approve'),
        (CANCEL, 'Cancel'),
        (DECLINE, 'Decline'),
    ]


class TransactionStatus:
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    CANCELLED = 'CANCELLED'
    FAILED = 'FAILED'
    REVERSED = 'REVERSED'
    FLAGGED = 'FLAGGED'

    CHOICES = [
        (PENDING, 'Pending'),
        (SUCCESS, 'Success'),
        (CANCELLED, 'Cancelled'),
        (FAILED, 'Failed'),
        (REVERSED, 'Reversed'),
        (FLAGGED, 'Flagged'),
    ]


class TransactionType:
    INTERNAL_TRANSFER = 'INTERNAL_TRANSFER'
    EXTERNAL_TRANSFER = 'EXTERNAL_TRANSFER'
    INTERNAL_REQUEST = 'INTERNAL_REQUEST'
    EXTERNAL_REQUEST = 'EXTERNAL_REQUEST'
    CURRENCY_EXCHANGE = 'CURRENCY_EXCHANGE'
    TOPUP = 'TOPUP'
    WITHDRAW = 'WITHDRAW'
    REFUND = 'REFUND'
    BUY_AIRTIME = 'BUY_AIRTIME'

    CHOICES = [
        (INTERNAL_TRANSFER, 'Send Money'),
        (EXTERNAL_TRANSFER, 'Send to M-Pesa / Bank'),
        (INTERNAL_REQUEST, 'Request Money'),
        (EXTERNAL_REQUEST, 'Request from M-Pesa / Bank'),
        (CURRENCY_EXCHANGE, 'Swap Currencies'),
        (TOPUP, 'Add Funds'),
        (WITHDRAW, 'Withdraw Funds'),
        (REFUND, 'Get a Refund'),
        (BUY_AIRTIME, 'Top Up Airtime'),
    ]
