import logging
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Avg, Max, Min, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from drf_spectacular.utils import extend_schema

from tracking.models import Activity
from tracking.serializers import ActivityStatsSerializer

logger = logging.getLogger(__name__)

@extend_schema(tags=['Tracking - Activity Stats'])
class ActivityStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @method_decorator(cache_page(60 * 15))
    @extend_schema(
        operation_id='Get Activity Statistics',
        description='Retrieve aggregated statistics about user activities.',
        request=None,
        responses={
            200: ActivityStatsSerializer,
            400: {'description': 'Bad Request'},
            401: {'description': 'Unauthorized'},
            403: {'description': 'Forbidden'},
            404: {'description': 'Not Found'},
            500: {'description': 'Internal Server Error'}
        }
    )
    def get(self, request):
        try:
            time_threshold = timezone.now() - timedelta(days=30)
            
            # Prepare raw data and convert QuerySets to lists
            raw_data = {
                'counts': {
                    'total': Activity.objects.count(),
                    'flagged': Activity.objects.filter(flagged=True).count(),
                    'last_30_days': Activity.objects.filter(timestamp__gte=time_threshold).count(),
                },
                'response_times': Activity.objects.aggregate(
                    avg=Avg('duration'), max=Max('duration'), min=Min('duration')),
                'types': list(Activity.objects.values('type')
                            .annotate(count=Count('type'))
                            .order_by('-count')),
                'endpoints': list(Activity.objects.values('endpoint', 'method')
                              .annotate(
                                  count=Count('id'), 
                                  avg_time=Avg('duration'),
                                  errors=Count('id', filter=Q(status__gte=400))
                              )
                              .order_by('-count')[:10]),
                'geography': list(Activity.objects.exclude(country='')
                              .values('country')
                              .annotate(count=Count('id'))
                              .order_by('-count')[:5]),
                'devices': list(Activity.objects.exclude(device='')
                            .values('device', 'os', 'browser')
                            .annotate(count=Count('id'))
                            .order_by('-count')[:5]),
                'users': list(Activity.objects.exclude(user__isnull=True)
                          .values('user__email')
                          .annotate(count=Count('id'))
                          .order_by('-count')[:5]),
            }

            # Serialize the data
            serializer = ActivityStatsSerializer(data={
                'counts': raw_data['counts'],
                'response_times': raw_data['response_times'],
                'types': raw_data['types'],
                'endpoints': raw_data['endpoints'],
                'geography': raw_data['geography'],
                'devices': raw_data['devices'],
                'users': raw_data['users'],
            })
            
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Failed to generate stats: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Failed to generate activity statistics'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
