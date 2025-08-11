# Third-party imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from drf_spectacular.utils import extend_schema

# Project imports
from rbac.permissions import MethodPermission, register_permissions
from userservice.models import User
from userservice.serializers import UserProfileStandardSerializer


@register_permissions
@extend_schema(tags=["User Services - User Management"])
class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = UserProfileStandardSerializer

    # Method-specific permissions for implemented methods only
    get_permission = 'list_users'

    @extend_schema(
        request=None,
        responses=UserProfileStandardSerializer(many=True),
        operation_id="Admin - List All Users",
        description="Retrieve a paginated list of all registered users."
    )
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        if not users.exists():
            return Response({"message": "No users found."}, status=status.HTTP_404_NOT_FOUND)

        paginator = LimitOffsetPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serialized_data = self.serializer_class(paginated_users, many=True).data

        return paginator.get_paginated_response(serialized_data)
