# views/card_views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from cardservice.serializers import LinkCardSerializer
from cardservice.services import TokenizationService
from cardservice.models import PaymentCard


class LinkCardView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LinkCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        tokenized = TokenizationService.tokenize_card(
            data['card_number'], data['expiry_month'], data['expiry_year'], data['cvv']
        )

        card = PaymentCard.objects.create(
            user=request.user,
            card_token=tokenized['token'],
            last_four=tokenized['last_four'],
            card_type=tokenized['card_type'],
            expiry_month=data['expiry_month'],
            expiry_year=data['expiry_year']
        )

        return Response({'card_id': card.id, 'card_token': tokenized['token']}, status=201)