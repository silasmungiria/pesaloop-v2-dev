# Standard library imports
from datetime import datetime, timedelta

# Third-party library imports
from django.db import models
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from userservice.models import User
from walletservice.models import DigitalWallet
from paymentservice.models import TransactionRecord
from reportingservice.utils import STATEMENT_PERIOD_DAYS
from reportingservice.serializers import TransactionReportSerializer
from .statement_exports import (
  BasePDFContentBuilder,
  generate_csv_report,
  generate_pdf_report
)


@register_permissions
@extend_schema(tags=["Reporting Services - Export Statement"])
class ExportTransactionStatementView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = TransactionReportSerializer

    # Method-specific permissions for implemented methods only
    get_permission = 'export_transaction_statement'

    @extend_schema(
        request=None,
        responses=TransactionReportSerializer(many=True),
        operation_id="Export Transaction Statement",
        description="Export transaction statement for the authenticated user."
    )
    def get(self, request):
        export_format = request.query_params.get('export_format', 'pdf').lower()
        delivery_method = request.query_params.get('delivery_method', 'download').lower()

        if export_format not in ['csv', 'pdf'] or delivery_method not in ['download', 'email']:
            return Response({"error": "Invalid export format or delivery method."}, status=400)

        try:
            user = User.objects.get(id=request.user.id)
            wallets = DigitalWallet.objects.all() if user.is_staff else DigitalWallet.objects.filter(wallet_owner=user)

            if not wallets.exists():
                return Response({"error": "No wallets found for this user."}, status=404)

            start_date = timezone.now() - timedelta(days=STATEMENT_PERIOD_DAYS)
            transactions = TransactionRecord.objects.filter(
                (models.Q(sender_wallet__in=wallets) | models.Q(receiver_wallet__in=wallets))
            ).filter(created_at__gte=start_date).order_by('-created_at')

            if not transactions.exists():
                return Response({"message": "No transactions found."}, status=404)

            filename_prefix = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user.get_full_name().lower().replace(' ', '-')}_txn"

            if export_format == 'csv':
                result = generate_csv_report(
                    transactions, request=request, filename=f"{filename_prefix}.csv", email=(delivery_method == 'email'))
            else:
                result = generate_pdf_report(
                    transactions, wallets, request=request, filename=f"{filename_prefix}.pdf", pdf_view=BasePDFContentBuilder(), email=(delivery_method == 'email'))

            if isinstance(result, dict):
                return Response(result)
            return result

        except Exception as e:
            return Response({"error": str(e)}, status=500)
