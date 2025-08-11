from decimal import Decimal
from data_encryption.services import EncryptionService


class DefaultConfig:
    """
    Encrypted defaults for wallets and customers.
    """

    BALANCE = Decimal('0.00')
    VERIFIED = True
    UNVERIFIED = False

    @staticmethod
    def balance():
        """Encrypted default wallet balance."""
        return EncryptionService.encrypt(str(DefaultConfig.BALANCE))

    @staticmethod
    def verified():
        """Encrypted default verified status."""
        return EncryptionService.encrypt(str(DefaultConfig.VERIFIED))

    @staticmethod
    def unverified():
        """Encrypted default unverified status."""
        return EncryptionService.encrypt(str(DefaultConfig.UNVERIFIED))
