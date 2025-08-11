from decimal import Decimal
from data_encryption.services import EncryptionService


class ZeroBalanceConfig:
    """
    Configuration for initializing wallet balances at zero.
    """
    DEFAULT_BALANCE = Decimal('0.00')

    @staticmethod
    def encrypted_balance():
        """
        Returns the encrypted default wallet balance (zero).
        """
        return EncryptionService.encrypt(str(ZeroBalanceConfig.DEFAULT_BALANCE))