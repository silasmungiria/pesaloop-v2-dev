from rest_framework import serializers
from paymentservice.models import TransactionRecord
from .wallet import WalletSerializer


class TransactionRecordsSerializer(serializers.ModelSerializer):
    """Serializer for fund transaction records."""
    sender_wallet = serializers.SerializerMethodField()
    receiver_wallet = serializers.SerializerMethodField()
    is_debit = serializers.SerializerMethodField()
    transaction_charge = serializers.SerializerMethodField()

    class Meta:
        model = TransactionRecord
        fields = [
            'id', 'sender_wallet', 'receiver_wallet', 'amount', 'currency', 
            'reference_id', 'transaction_charge', 'status', 'payment_provider', 
            'reason', 'transaction_type', 'created_at', 'updated_at', 'is_debit'
        ]

    def get_sender_wallet(self, obj):
        """Return serialized sender wallet details."""
        return WalletSerializer(obj.sender_wallet).data

    def get_receiver_wallet(self, obj):
        """Return serialized receiver wallet details."""
        return WalletSerializer(obj.receiver_wallet).data

    def get_is_debit(self, obj):
        """Return True if the authenticated user owns the sender wallet."""
        request = self.context.get('request')
        return request and request.user == obj.sender_wallet.wallet_owner

    def get_transaction_charge(self, obj):
        """Return transaction charge if the authenticated user is not the sender."""
        return None if not self.get_is_debit(obj) else obj.transaction_charge