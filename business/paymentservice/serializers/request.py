from rest_framework import serializers
from .. import models

class RequestedTransactionSerializer(serializers.ModelSerializer):
    requesting_user = serializers.SerializerMethodField()
    requested_user = serializers.SerializerMethodField()

    class Meta:
        model = models.RequestedTransaction
        fields = [
            'id', 'requesting_user', 'requested_user', 'amount',
            'currency', 'status', 'reference_id', 'payment_provider',
            'action', 'reason', 'created_at', 'updated_at'
        ]
        read_only_fields = fields

    def get_requesting_user(self, obj):
        return {
            'id': obj.requesting_user.id,
            'full_name': obj.requesting_user.get_full_name(),
            'email': obj.requesting_user.email,
            'phone_number': obj.requesting_user.phone_number
        }

    def get_requested_user(self, obj):
        return {
            'id': obj.requested_user.id,
            'full_name': obj.requested_user.get_full_name(),
            'email': obj.requested_user.email,
            'phone_number': obj.requested_user.phone_number
        }
