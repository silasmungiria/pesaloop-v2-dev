# views/transaction_views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from cardservice.serializers import PaymentSerializer
from cardservice.services import TransactionService
from cardservice.models import PaymentCard


class ProcessPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        card = PaymentCard.objects.get(id=data['card_id'], user=request.user, is_active=True)

        txn = TransactionService().process_payment(
            user=request.user,
            card=card,
            amount=data['amount']
        )

        return Response({'transaction_reference': txn.transaction_reference, 'status': txn.status})