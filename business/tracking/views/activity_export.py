import csv
import logging
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter

from tracking.models import Activity
from tracking.serializers import ActivityListSerializer
from tracking.views.activity_list import ActivityListView

logger = logging.getLogger(__name__)

@extend_schema(tags=['Tracking - Export Activities'])
class ActivityExportView(GenericViewSet):
    queryset = Activity.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ActivityListSerializer
    filter_backends = [SearchFilter]
    filterset_fields = ActivityListView.filterset_fields
    search_fields = ActivityListView.search_fields

    @extend_schema(
        operation_id='Export Activities',
        description='Export user activities in CSV or JSON format.',
        request=None,
        parameters=[
            OpenApiParameter(
                name='format',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Export format (csv or json)',
                default='csv'
            ),
        ],
        responses={
            200: {
                'description': 'CSV or JSON export of activities',
                'content': {
                    'text/csv': {'schema': {'type': 'string'}},
                    'application/json': {'schema': {'type': 'object'}}
                }
            }
        }
    )
    @action(detail=False, methods=['get'])
    def export(self, request):
        try:
            format = request.query_params.get('format', 'csv').lower()
            queryset = self.filter_queryset(self.get_queryset())

            if format == 'json':
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)

            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'attachment; filename="activities.csv"'},
            )

            writer = csv.writer(response)
            writer.writerow([
                'ID', 'Timestamp', 'Type', 'User Email', 'IP Address',
                'Country', 'Region', 'City', 'Coordinates',
                'Endpoint', 'Method', 'Status', 'Duration (ms)',
                'Device', 'OS', 'Browser', 'Is Mobile',
                'Flagged', 'Tags', 'User Agent'
            ])

            for activity in queryset:
                writer.writerow([
                    str(activity.id),
                    activity.timestamp.isoformat(),
                    activity.get_type_display(),
                    activity.user.email if activity.user else '',
                    activity.ip_address,
                    activity.country,
                    activity.region,
                    activity.city,
                    activity.coordinates,
                    activity.endpoint,
                    activity.method,
                    activity.status,
                    round(activity.duration * 1000, 2) if activity.duration else '',
                    activity.device,
                    activity.os,
                    activity.browser,
                    'Yes' if activity.is_mobile else 'No' if activity.is_mobile is not None else '',
                    'Yes' if activity.flagged else 'No',
                    '|'.join(activity.tags) if activity.tags else '',
                    activity.user_agent[:200] if activity.user_agent else '',
                ])

            return response

        except Exception as e:
            logger.error(f"Failed to export activities: {str(e)}", exc_info=True)
            return Response({'error': 'Failed to export activities'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
