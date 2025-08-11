from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListAPIView

from ..serializers import ExchangeRateSnapshotSerializer
from ..models import RateSnapshot


@extend_schema(
    tags=["Forex Services - Update Rates"],
    operation_id="Fetch Exchange Rates",
    description="Fetch all exchange rates with pagination support.",
    responses=ExchangeRateSnapshotSerializer
)
class AdminRatesView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ExchangeRateSnapshotSerializer
    queryset = RateSnapshot.objects.all()
