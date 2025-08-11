from rest_framework import serializers
from decimal import Decimal
from .. import models as wallet_models


class WalletSerializer(serializers.ModelSerializer):
    wallet_owner = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    class Meta:
        model = wallet_models.DigitalWallet
        fields = ['id', 'wallet_owner', 'balance', 'currency', 'is_default', 'is_active', 'last_updated', 'created_at']
        read_only_fields = fields

    def get_wallet_owner(self, obj):
        return {
            'user_id': obj.wallet_owner.id,
            'name': obj.wallet_owner.get_full_name(),
            'email': obj.wallet_owner.email,
            'phone_number': obj.wallet_owner.phone_number,
        }

    def get_currency(self, obj):
        return {
            'name': obj.currency.name,
            'code': obj.currency.code
        }
