from decimal import Decimal

class TransactionFeeConfig:
    """
    Configuration for transaction fees.
    """
    TRANSACTION_FEE_RATE = Decimal('0.015')                  # 1.5%
    MAX_TRANSACTION_FEE = Decimal('500')                     # Max fee
    FEE_FLAT_THRESHOLD_AMOUNT = Decimal('100000')            # Flat fee threshold


class TransferLimits:
    """
    Configuration for transfer limits.
    """
    UNVERIFIED_WALLET_MAX_TRANSFER = Decimal('150.00')       # Max allowed for unverified wallets
