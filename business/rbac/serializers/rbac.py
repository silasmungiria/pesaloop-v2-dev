from rest_framework import serializers
from rbac.models import Permission, Role, RolePermission, UserRole
from userservice.serializers import UserProfileStandardSerializer, UserProfilePublicSerializer


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'codename',
            'category',
            'method',
            'description',
            'is_sensitive'
        ]
        read_only_fields = ['id']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
            'name',
            'description',
            'level',
            'is_default'
        ]
        read_only_fields = ['id']

class RolePermissionSerializer(serializers.ModelSerializer):
    granted_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    permission = PermissionSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    granted_by = UserProfilePublicSerializer(read_only=True)
    permission_count = serializers.SerializerMethodField()

    class Meta:
        model = RolePermission
        fields = [
            'id',
            'role',
            'permission',
            'granted_by',
            'permission_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'permission_count', 'granted_by', 'created_at', 'updated_at'
        ]

    def get_permission_count(self, obj):
        return RolePermission.objects.filter(role=obj.role).count()

class UserRoleSerializer(serializers.ModelSerializer):
    assigned_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    user = UserProfilePublicSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    assigned_by = UserProfilePublicSerializer(read_only=True)
    role_count = serializers.SerializerMethodField()

    class Meta:
        model = UserRole
        fields = [
            'id', 
            'user',
            'role',
            'role_count',
            'assigned_by',
            'is_active',
            'notes',
            'assigned_at',
            'expires_at'
        ]
        read_only_fields = [
            'id', 'role_count', 'assigned_by', 'assigned_at'
        ]

    def get_role_count(self, obj):
        return UserRole.objects.filter(user=obj.user).count()
