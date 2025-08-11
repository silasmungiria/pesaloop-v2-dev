import logging
from rest_framework import permissions, status
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema

from tracking.models import Activity

logger = logging.getLogger(__name__)

@extend_schema(tags=['Tracking - Delete Activity'])
class ActivityDeleteView(DestroyAPIView):
    queryset = Activity.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

    @extend_schema(
        operation_id='Delete Activity',
        description='Delete a specific user activity by ID.',
        request=None,
        responses={
            204: {'description': 'Activity deleted successfully'},
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
        logger.error(f"Failed to delete activity: {str(exc)}", exc_info=True)
        return Response({'error': 'Failed to delete activity'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
