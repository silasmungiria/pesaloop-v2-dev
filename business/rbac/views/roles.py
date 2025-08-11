from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view

from rbac.models import Role, RolePermission
from rbac.permissions import MethodPermission, register_permissions
from rbac.serializers import RoleSerializer
from .mixins import AuditMixin


@register_permissions
@extend_schema_view(
    list=extend_schema(
        tags=["RBAC - Roles"],
        operation_id="List Roles",
        description="List all roles.",
        responses={status.HTTP_200_OK: RoleSerializer(many=True)}
    ),
    retrieve=extend_schema(
        tags=["RBAC - Roles"],
        operation_id="Retrieve Role",
        description="Retrieve a specific role by ID.",
        responses={status.HTTP_200_OK: RoleSerializer}
    ),
    create=extend_schema(
        tags=["RBAC - Roles"],
        operation_id="Create Role",
        description="Create a new role.",
        request=RoleSerializer,
        responses={status.HTTP_201_CREATED: RoleSerializer}
    ),
    update=extend_schema(
        tags=["RBAC - Roles"],
        operation_id="Update Role",
        description="Update an existing role.",
        request=RoleSerializer,
        responses={status.HTTP_200_OK: RoleSerializer}
    ),
    partial_update=extend_schema(
        tags=["RBAC - Roles"],
        operation_id="Partial Update Role",
        description="Partially update a role.",
        request=RoleSerializer,
        responses={status.HTTP_200_OK: RoleSerializer}
    ),
    destroy=extend_schema(
        tags=["RBAC - Roles"],
        operation_id="Delete Role",
        description="Delete a role by ID.",
        responses={status.HTTP_204_NO_CONTENT: "Role deleted successfully"}
    )
)
class RoleViewSet(AuditMixin, ModelViewSet):
    queryset = Role.objects.all()
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = RoleSerializer

    # Method-specific permissions
    get_permission = 'view_role'
    post_permission = 'add_role'
    put_permission = 'change_role'
    delete_permission = 'delete_role'
    required_permission = 'business_hours_access'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('level', 'name')

    @extend_schema(
        tags=["RBAC - Roles"],
        operation_id="Clone Role",
        description="Clone a role along with all its permissions.",
        responses={
            status.HTTP_201_CREATED: RoleSerializer,
            status.HTTP_403_FORBIDDEN: "You do not have permission to clone this role."
        }
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, MethodPermission])
    def clone(self, request, pk=None):
        clone_permission = 'add_role'
        if not request.user.has_perm(clone_permission):
            return Response(
                {"message": f"You need the '{clone_permission}' permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        role = self.get_object()
        new_role = Role.objects.create(
            name=f"{role.name} (Copy)",
            description=role.description,
            level=role.level,
            is_default=False
        )

        for rp in role.permissions.all():
            RolePermission.objects.create(
                role=new_role,
                permission=rp.permission,
                granted_by=request.user
            )

        serializer = self.get_serializer(new_role)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
