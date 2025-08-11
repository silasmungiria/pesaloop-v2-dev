# serializers/payment_serializer.py
from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    card_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)