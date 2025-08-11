from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from rbac.models import Permission
from rbac.permissions import MethodPermission, register_permissions
from rbac.serializers import PermissionSerializer
from rbac.utils import PERMISSION_CATEGORIES
from .mixins import AuditMixin


@register_permissions
@extend_schema_view(
    list=extend_schema(
        tags=["RBAC - Permissions"],
        operation_id="List Permissions",
        description="List all permissions with optional filtering by category.",
        responses={
            status.HTTP_200_OK: PermissionSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: "Validation error response",
            status.HTTP_404_NOT_FOUND: "No permissions found"
        }
    ),
    retrieve=extend_schema(
        tags=["RBAC - Permissions"],
        operation_id="Retrieve Permission",
        description="Retrieve a specific permission by ID.",
        responses={
            status.HTTP_200_OK: PermissionSerializer,
            status.HTTP_404_NOT_FOUND: "Permission not found"
        }
    ),
    create=extend_schema(
        tags=["RBAC - Permissions"],
        operation_id="Create Permission",
        description="Create a new permission.",
        request=PermissionSerializer,
        responses={
            status.HTTP_201_CREATED: PermissionSerializer,
            status.HTTP_400_BAD_REQUEST: "Validation error response"
        }
    ),
    update=extend_schema(
        tags=["RBAC - Permissions"],
        operation_id="Update Permission",
        description="Update an existing permission.",
        request=PermissionSerializer,
        responses={
            status.HTTP_200_OK: PermissionSerializer,
            status.HTTP_400_BAD_REQUEST: "Validation error response",
            status.HTTP_404_NOT_FOUND: "Permission not found"
        }
    ),
    partial_update=extend_schema(
        tags=["RBAC - Permissions"],
        operation_id="Partial Update Permission",
        description="Partially update an existing permission.",
        request=PermissionSerializer,
        responses={
            status.HTTP_200_OK: PermissionSerializer,
            status.HTTP_400_BAD_REQUEST: "Validation error response",
            status.HTTP_404_NOT_FOUND: "Permission not found"
        }
    ),
    destroy=extend_schema(
        tags=["RBAC - Permissions"],
        operation_id="Delete Permission",
        description="Delete a specific permission by ID.",
        responses={
            status.HTTP_204_NO_CONTENT: "Permission deleted successfully",
            status.HTTP_404_NOT_FOUND: "Permission not found"
        }
    )
)
class PermissionViewSet(AuditMixin, ModelViewSet):
    queryset = Permission.objects.all()
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = PermissionSerializer

    # Method-specific permissions
    get_permission = 'view_permission'
    post_permission = 'add_permission'
    put_permission = 'change_permission'
    delete_permission = 'delete_permission'
    required_permission = 'business_hours_access'

    def get_queryset(self):
        queryset = super().get_queryset()
        if category := self.request.query_params.get('category'):
            queryset = queryset.filter(category=category)
        return queryset.order_by('category', 'name')

    @extend_schema(
        tags=["RBAC - Permissions"],
        operation_id="List Permission Categories",
        description="Get available permission categories.",
        responses={status.HTTP_200_OK: "List of permission categories"}
    )
    @action(detail=False, methods=["get"])
    def categories(self, request):
        return Response([{'value': c[0], 'label': c[1]} for c in PERMISSION_CATEGORIES])

    @extend_schema(
        tags=["RBAC - Permissions"],
        operation_id="List Permission Methods",
        description="Get available HTTP methods for permissions.",
        responses={status.HTTP_200_OK: "List of HTTP methods"}
    )
    @action(detail=False, methods=["get"])
    def methods(self, request):
        return Response([{'value': m[0], 'label': m[1]} for m in Permission.Method.choices])
