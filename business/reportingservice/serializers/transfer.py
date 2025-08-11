from rest_framework import serializers
from paymentservice.models import RequestedTransaction
from .base import UserSerializer


class TransferRequestSerializer(serializers.ModelSerializer):
    """Serializer for fund transfer requests."""
    requesting_user = serializers.SerializerMethodField()
    requested_user = serializers.SerializerMethodField()
    is_debit = serializers.SerializerMethodField()

    class Meta:
        model = RequestedTransaction
        fields = [
            'id', 'requesting_user', 'requested_user', 'amount', 'currency', 
            'status', 'reference_id', 'payment_provider', 'action', 'reason', 
            'transaction_type', 'is_debit', 'created_at', 'updated_at'
        ]

    def get_requesting_user(self, obj):
        """Return serialized details of the requesting user."""
        return UserSerializer(obj.requesting_user).data

    def get_requested_user(self, obj):
        """Return serialized details of the requested user."""
        return UserSerializer(obj.requested_user).data

    def get_is_debit(self, obj):
        """Return True if the authenticated user initiated the request."""
        request = self.context.get('request')
        return request and request.user == obj.requested_user