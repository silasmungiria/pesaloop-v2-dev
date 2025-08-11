from rest_framework import serializers
from ..utils import RequestAction

class TransferRequestActionSerializer(serializers.Serializer):
    request_id = serializers.UUIDField(write_only=True, required=True)
    action = serializers.ChoiceField(choices=RequestAction.CHOICES, write_only=True, required=True)
