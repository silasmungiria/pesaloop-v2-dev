from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from rbac.models import UserRole
from rbac.permissions import MethodPermission, BusinessHoursAccessPermission, register_permissions
from rbac.serializers import UserRoleSerializer
from rbac.services import RoleAssignmentService
from .mixins import AuditMixin


@register_permissions
@extend_schema_view(
    list=extend_schema(
        tags=["RBAC - User Roles"],
        operation_id="List User Roles",
        description="List all user-role assignments.",
        responses={status.HTTP_200_OK: UserRoleSerializer(many=True)}
    ),
    retrieve=extend_schema(
        tags=["RBAC - User Roles"],
        operation_id="Retrieve User Role",
        description="Retrieve a specific user-role assignment.",
        responses={status.HTTP_200_OK: UserRoleSerializer}
    ),
    create=extend_schema(
        tags=["RBAC - User Roles"],
        operation_id="Create User Role",
        description="Assign a role to a user.",
        request=UserRoleSerializer,
        responses={
            status.HTTP_201_CREATED: UserRoleSerializer,
            status.HTTP_400_BAD_REQUEST: "Validation error or role assignment failed"
        }
    ),
    update=extend_schema(
        tags=["RBAC - User Roles"],
        operation_id="Update User Role",
        description="Update a user-role assignment.",
        request=UserRoleSerializer,
        responses={status.HTTP_200_OK: UserRoleSerializer}
    ),
    partial_update=extend_schema(
        tags=["RBAC - User Roles"],
        operation_id="Partial Update User Role",
        description="Partially update a user-role assignment.",
        request=UserRoleSerializer,
        responses={status.HTTP_200_OK: UserRoleSerializer}
    ),
    destroy=extend_schema(
        tags=["RBAC - User Roles"],
        operation_id="Delete User Role",
        description="Delete a user-role assignment.",
        responses={status.HTTP_204_NO_CONTENT: "User role deleted successfully"}
    )
)
class UserRoleViewSet(AuditMixin, ModelViewSet):
    queryset = UserRole.objects.select_related('user', 'role', 'assigned_by')
    permission_classes = [IsAuthenticated, MethodPermission, BusinessHoursAccessPermission]
    serializer_class = UserRoleSerializer

    # Method-specific permissions
    get_permission = 'view_userrole'
    post_permission = 'add_userrole'
    put_permission = 'change_userrole'
    delete_permission = 'delete_userrole'
    required_permission = 'past_business_hours_access'

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset.order_by('-assigned_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            RoleAssignmentService.assign_role(
                user=serializer.validated_data['user'],
                role=serializer.validated_data['role'],
                assigned_by=request.user,
                expires_at=serializer.validated_data.get('expires_at')
            )
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        tags=["RBAC - User Roles"],
        operation_id="Deactivate User Role",
        description="Deactivate a user-role assignment.",
        responses={status.HTTP_200_OK: "Role deactivated successfully"}
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, MethodPermission])
    def deactivate(self, request, pk=None):
        user_role = self.get_object()
        user_role.is_active = False
        user_role.save()
        return Response({'status': 'role deactivated'})

    @extend_schema(
        tags=["RBAC - User Roles"],
        operation_id="Activate User Role",
        description="Activate a previously deactivated user-role assignment.",
        responses={status.HTTP_200_OK: "Role activated successfully"}
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, MethodPermission])
    def activate(self, request, pk=None):
        user_role = self.get_object()
        user_role.is_active = True
        user_role.save()
        return Response({'status': 'role activated'})
