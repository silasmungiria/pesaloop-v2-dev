import logging
from rest_framework import permissions, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema

from tracking.models import Activity
from tracking.serializers import ActivitySerializer

logger = logging.getLogger(__name__)

@extend_schema(tags=['Tracking - Activity Details'])
class ActivityDetailView(RetrieveAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

    @extend_schema(
        operation_id='Retrieve Activity Details',
        description='Get detailed information about a specific user activity by ID.',
        request=None,
        responses={
            200: ActivitySerializer,
            400: {'description': 'Bad Request'},
            401: {'description': 'Unauthorized'},
            403: {'description': 'Forbidden'},
            404: {'description': 'Activity not found'},
            500: {'description': 'Internal Server Error'}
        }
    )
    def handle_exception(self, exc):
        if isinstance(exc, ObjectDoesNotExist):
            return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
        logger.error(f"Failed to retrieve activity: {str(exc)}", exc_info=True)
        return Response({'error': 'Failed to retrieve activity details'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
