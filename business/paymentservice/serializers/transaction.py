from rest_framework import serializers
from .. import models

class TransactionRecordSerializer(serializers.ModelSerializer):
    sender_wallet = serializers.SerializerMethodField()
    receiver_wallet = serializers.SerializerMethodField()

    class Meta:
        model = models.TransactionRecord
        fields = [
            'id',
            'sender_wallet',
            'receiver_wallet',
            'amount',
            'reference_id',
            'transaction_charge',
            'currency',
            'status',
            'transaction_type',
            'payment_provider',
            'reason',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields

    def get_sender_wallet(self, obj):
        if obj.sender_wallet:
            return {
                'wallet_id': obj.sender_wallet.id,
                'wallet_owner': obj.sender_wallet.wallet_owner.get_full_name(),
                "currency": obj.sender_wallet.currency.code,
                'currency_name': obj.sender_wallet.currency.name,
                'is_default': obj.sender_wallet.is_default,
            }
        return None

    def get_receiver_wallet(self, obj):
        if obj.receiver_wallet:
            return {
                'wallet_id': obj.receiver_wallet.id,
                'wallet_owner': obj.receiver_wallet.wallet_owner.get_full_name(),
                "currency": obj.receiver_wallet.currency.code,
                'currency_name': obj.receiver_wallet.currency.name,
                'is_default': obj.receiver_wallet.is_default,
            }
        return None
