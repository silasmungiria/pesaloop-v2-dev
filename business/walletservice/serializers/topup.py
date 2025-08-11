from rest_framework import serializers
from decimal import Decimal

from userservice import models as user_models
from .. import models as wallet_models


class DevelopmentWalletTopUpSerializer(serializers.Serializer):
    amount = serializers.DecimalField(min_value=Decimal("0.00"), max_digits=30, decimal_places=2)
    currency = serializers.PrimaryKeyRelatedField(queryset=wallet_models.Currency.objects.all())
    wallet_owner = serializers.PrimaryKeyRelatedField(queryset=user_models.User.objects.all())
