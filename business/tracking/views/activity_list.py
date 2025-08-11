import logging
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from tracking.models import Activity
from tracking.serializers import ActivityListSerializer
from tracking.views.throttles import BurstRateThrottle, SustainedRateThrottle

logger = logging.getLogger(__name__)

@extend_schema(tags=['Tracking - Activity List'])
class ActivityListView(ListAPIView):
    queryset = Activity.objects.all().order_by('-timestamp')
    serializer_class = ActivityListSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = {
        'type': ['exact', 'in'],
        'user': ['exact'],
        'ip_address': ['exact', 'contains', 'startswith'],
        'flagged': ['exact'],
        'timestamp': ['gte', 'lte', 'exact', 'range'],
        'country': ['exact', 'in'],
        'status': ['exact', 'gte', 'lte'],
        'method': ['exact', 'in'],
        'is_mobile': ['exact'],
        'is_bot': ['exact'],
    }
    search_fields = [
        'user__email', 'ip_address', 'endpoint', 'device',
        'browser', 'city', 'tags', 'user_agent',
    ]
    ordering_fields = ['timestamp', 'duration', 'status', 'type']
    ordering = ['-timestamp']
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    @extend_schema(
        operation_id='List Activities',
        description='Retrieve a paginated list of user activities with optional filtering and sorting.',
        parameters=[
            OpenApiParameter(name='page', type=int, location=OpenApiParameter.QUERY, description='Page number'),
            OpenApiParameter(name='page_size', type=int, location=OpenApiParameter.QUERY, description='Number of results per page'),
        ],
        responses=ActivityListSerializer(many=True)
    )
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to list activities: {str(e)}", exc_info=True)
            return Response({'error': 'Failed to retrieve activities'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
