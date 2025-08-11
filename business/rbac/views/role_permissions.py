from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from rbac.models import Permission, RolePermission
from rbac.permissions import MethodPermission, register_permissions
from rbac.serializers import RolePermissionSerializer, PermissionSerializer
from .mixins import AuditMixin


@register_permissions
@extend_schema_view(
    list=extend_schema(
        tags=["RBAC - Role Permissions"],
        operation_id="List Role Permissions",
        description="List all role-permission assignments.",
        responses={status.HTTP_200_OK: RolePermissionSerializer(many=True)}
    ),
    retrieve=extend_schema(
        tags=["RBAC - Role Permissions"],
        operation_id="Retrieve Role Permission",
        description="Retrieve a specific role-permission assignment.",
        responses={status.HTTP_200_OK: RolePermissionSerializer}
    ),
    create=extend_schema(
        tags=["RBAC - Role Permissions"],
        operation_id="Create Role Permission",
        description="Assign a permission to a role.",
        request=RolePermissionSerializer,
        responses={
            status.HTTP_201_CREATED: RolePermissionSerializer,
            status.HTTP_400_BAD_REQUEST: "Validation error"
        }
    ),
    update=extend_schema(
        tags=["RBAC - Role Permissions"],
        operation_id="Update Role Permission",
        description="Update a role-permission assignment.",
        request=RolePermissionSerializer,
        responses={status.HTTP_200_OK: RolePermissionSerializer}
    ),
    partial_update=extend_schema(
        tags=["RBAC - Role Permissions"],
        operation_id="Partial Update Role Permission",
        description="Partially update a role-permission assignment.",
        request=RolePermissionSerializer,
        responses={status.HTTP_200_OK: RolePermissionSerializer}
    ),
    destroy=extend_schema(
        tags=["RBAC - Role Permissions"],
        operation_id="Delete Role Permission",
        description="Remove a role-permission assignment.",
        responses={status.HTTP_204_NO_CONTENT: "Role permission deleted successfully"}
    )
)
class RolePermissionViewSet(AuditMixin, ModelViewSet):
    queryset = RolePermission.objects.select_related('role', 'permission', 'granted_by')
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = RolePermissionSerializer

    # Method-specific permissions
    get_permission = 'view_rolepermission'
    post_permission = 'add_rolepermission'
    put_permission = 'change_rolepermission'
    delete_permission = 'delete_rolepermission'
    required_permission = 'business_hours_access'

    def get_queryset(self):
        queryset = super().get_queryset()
        role_id = self.request.query_params.get('role_id')
        if role_id:
            queryset = queryset.filter(role=role_id)
        return queryset.order_by('role', 'permission')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        tags=["RBAC - Role Permissions"],
        operation_id="List Available Permissions for Role",
        description="Get permissions not yet assigned to a given role.",
        responses={
            status.HTTP_200_OK: PermissionSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: "role_id parameter is required"
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, MethodPermission])
    def available(self, request):
        role_id = request.query_params.get('role_id')
        if not role_id:
            return Response(
                {"message": "role_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        assigned_perms = RolePermission.objects.filter(
            role=role_id
        ).values_list('permission_id', flat=True)

        available_perms = Permission.objects.exclude(
            id__in=assigned_perms
        ).order_by('category', 'name')

        serializer = PermissionSerializer(available_perms, many=True)
        return Response(serializer.data)
