from rest_framework import serializers
from walletservice import models as wallet_models
from .base import UserSerializer
from .currency import CurrencySerializer


class WalletSerializer(serializers.ModelSerializer):
    """Serializer for wallet details."""
    wallet_owner = UserSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = wallet_models.DigitalWallet
        fields = ['id', 'wallet_owner', 'currency']
        read_only_fields = fields