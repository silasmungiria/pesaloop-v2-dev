from decimal import Decimal
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from creditservice.models import Loan, Repayment
from creditservice.serializers import LoanRequestSerializer, LoanSerializer, RepaymentSerializer
from creditservice.services import LoanCalculator, ReconciliationService
from creditservice.utils import LoanStatus
from rbac.permissions import MethodPermission, register_permissions


@register_permissions
@extend_schema(
    tags=['Credit Service - Loans'],
    operation_id="Request Loan",
    description="Submit a new loan request.",
    request=LoanRequestSerializer,
    responses={
        status.HTTP_201_CREATED: LoanSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
        status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT
    }
)
class LoanRequestAPIView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = LoanRequestSerializer
    response_serializer_class = LoanSerializer
    post_permission = 'request_loan'

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        credit_profile = request.user.credit_profile
        if not credit_profile.is_loan_qualified:
            return Response({"error": "User is not qualified for loans"}, status=status.HTTP_403_FORBIDDEN)

        with transaction.atomic():
            loan = Loan.objects.create(user=credit_profile, amount=serializer.validated_data['amount'])

        return Response(self.response_serializer_class(loan).data, status=status.HTTP_201_CREATED)


@register_permissions
@extend_schema(
    tags=['Credit Service - Loans'],
    operation_id="Approve Loan",
    description="Approve a pending loan application.",
    parameters=[
        OpenApiParameter(name='loan_id', type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)
    ],
    responses={
        status.HTTP_200_OK: LoanSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
        status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT
    }
)
class LoanApprovalAPIView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    response_serializer_class = LoanSerializer
    post_permission = 'approve_loan'

    def post(self, request, loan_id):
        try:
            with transaction.atomic():
                loan = Loan.objects.select_for_update().get(id=loan_id)

                if loan.status != LoanStatus.PENDING:
                    return Response({"error": "Only pending loans can be approved"}, status=status.HTTP_400_BAD_REQUEST)

                loan.status = LoanStatus.APPROVED
                loan.approved_by = request.user
                loan.approved_at = timezone.now()
                loan.save()

                return Response(self.response_serializer_class(loan).data, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)


@register_permissions
@extend_schema(
    tags=['Credit Service - Loans'],
    operation_id="Disburse Loan",
    description="Disburse an approved loan.",
    parameters=[
        OpenApiParameter(name='loan_id', type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)
    ],
    responses={
        status.HTTP_200_OK: LoanSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
        status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT
    }
)
class LoanDisbursementAPIView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    response_serializer_class = LoanSerializer
    post_permission = 'disburse_loan'

    def post(self, request, loan_id):
        try:
            with transaction.atomic():
                loan = Loan.objects.select_for_update().get(id=loan_id)

                if loan.status != LoanStatus.APPROVED:
                    return Response({"error": "Loan must be in approved state"}, status=status.HTTP_400_BAD_REQUEST)

                loan.status = LoanStatus.DISBURSED
                loan.disbursement_date = timezone.now().date()
                loan.due_date = loan.disbursement_date + timedelta(days=30)
                loan.save()

                LoanCalculator.generate_repayment_schedule(loan)

                return Response(self.response_serializer_class(loan).data, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)


@register_permissions
@extend_schema(
    tags=['Credit Service - Loans'],
    operation_id="Repay Loan",
    description="Make a repayment toward a loan.",
    parameters=[
        OpenApiParameter(name='loan_id', type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        OpenApiParameter(name='amount', type=OpenApiTypes.DECIMAL, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='payment_date', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY)
    ],
    responses={
        status.HTTP_200_OK: RepaymentSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
        status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT,
        status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT
    }
)
class LoanRepaymentAPIView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    response_serializer_class = RepaymentSerializer
    post_permission = 'process_loan_repayment'

    def post(self, request, loan_id):
        try:
            with transaction.atomic():
                loan = Loan.objects.select_related('user__user').get(id=loan_id)

                is_employer_admin = request.user.managed_employers.filter(id=loan.user.employer_id).exists()
                is_borrower = request.user == loan.user.user

                if not (is_employer_admin or is_borrower):
                    return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

                amount = request.data.get('amount')
                if not amount:
                    return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

                if is_employer_admin:
                    repayment = ReconciliationService.process_repayment(loan)
                else:
                    repayment = loan.repayments.filter(
                        status__in=[LoanStatus.PENDING, LoanStatus.PARTIAL]
                    ).order_by('due_date').first()

                    if not repayment:
                        return Response({"error": "No pending repayments found"}, status=status.HTTP_400_BAD_REQUEST)

                    repayment.amount_paid = (repayment.amount_paid or 0) + Decimal(amount)
                    repayment.payment_date = request.data.get('payment_date') or timezone.now().date()
                    repayment.save()

                    if loan.total_repayment >= loan.amount + loan.interest_accrued + loan.processing_fee:
                        loan.status = LoanStatus.REPAID
                        loan.save()

                return Response(self.response_serializer_class(repayment).data, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)


@register_permissions
@extend_schema(
    tags=['Credit Service - Loans'],
    operation_id="List My Loans",
    description="Retrieve the current user's loan history.",
    responses={
        status.HTTP_200_OK: LoanSerializer(many=True),
        status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT
    }
)
class UserLoanHistoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = LoanSerializer
    get_permission = 'view_own_loans'

    def get(self, request, *args, **kwargs):
        loans = Loan.objects.filter(user__user=request.user).prefetch_related('repayments').order_by('-created_at')
        return Response(self.serializer_class(loans, many=True).data, status=status.HTTP_200_OK)


@register_permissions
@extend_schema(
    tags=['Credit Service - Loans'],
    operation_id="List All Loans (Admin)",
    description="Retrieve all loans for admin users.",
    parameters=[
        OpenApiParameter(name='status', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='employer', type=OpenApiTypes.UUID, location=OpenApiParameter.QUERY)
    ],
    responses={
        status.HTTP_200_OK: LoanSerializer(many=True),
        status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT
    }
)
class AdminLoanListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = LoanSerializer
    filterset_fields = ['status', 'user__employer']
    search_fields = ['user__user__first_name', 'user__user__last_name', 'reference_number']
    get_permission = 'view_all_loans'

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(self.serializer_class(queryset, many=True).data, status=status.HTTP_200_OK)
