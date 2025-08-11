from rest_framework import serializers
from .. import models as wallet_models


class SetDefaultWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = wallet_models.DigitalWallet
        fields = ['is_default']

    def validate(self, data):
        if not data['is_default']:
            raise serializers.ValidationError("Cannot set wallet as default unless specified.")
        return data


class WalletActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = wallet_models.DigitalWallet
        fields = ['is_active']

    def validate(self, data):
        if not data['is_active']:
            raise serializers.ValidationError("Wallet is not activated.")
        return data
