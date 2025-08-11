from rest_framework import serializers
from .exchange import CurrencyExchangeSerializer
from .transfer import TransferRequestSerializer
from .transaction import TransactionRecordsSerializer


class TransactionReportSerializer(serializers.Serializer):
    """Serializer for transaction reports."""
    exchange_records = CurrencyExchangeSerializer(many=True)
    payment_requests = TransferRequestSerializer(many=True)
    transaction_records = TransactionRecordsSerializer(many=True)