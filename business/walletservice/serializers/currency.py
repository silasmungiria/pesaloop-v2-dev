from rest_framework import serializers
from .. import models as wallet_models


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = wallet_models.Currency
        fields = ['id', 'name', 'code']
