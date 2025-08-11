# serializers/card_serializer.py
from rest_framework import serializers

class LinkCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=19)
    expiry_month = serializers.IntegerField()
    expiry_year = serializers.IntegerField()
    cvv = serializers.CharField(max_length=4)