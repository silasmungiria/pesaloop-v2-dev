from django.core.exceptions import PermissionDenied
from rbac.models import Role, UserRole
from rbac.services import clear_permission_cache

class RoleAssignmentService:
    @classmethod
    def assign_role(cls, user, role, assigned_by=None, expires_at=None):
        if assigned_by and not cls.can_assign_role(assigned_by, role):
            raise PermissionDenied("You cannot assign this role")

        if UserRole.objects.filter(user=user, role=role).exists():
            return False

        UserRole.objects.create(
            user=user,
            role=role,
            assigned_by=assigned_by,
            expires_at=expires_at
        )
        clear_permission_cache(user)
        return True

    @classmethod
    def can_assign_role(cls, assigning_user, role):
        if assigning_user.is_superuser:
            return True

        user_roles = UserRole.objects.filter(
            user=assigning_user,
            is_active=True
        ).select_related('role')

        if not user_roles.exists():
            return False

        max_user_level = max(r.role.level for r in user_roles)
        return max_user_level >= role.level

    @classmethod
    def get_assignable_roles(cls, user):
        if user.is_superuser:
            return Role.objects.all()

        user_roles = UserRole.objects.filter(
            user=user,
            is_active=True
        ).select_related('role')

        if not user_roles.exists():
            return Role.objects.none()

        max_user_level = max(r.role.level for r in user_roles)
        return Role.objects.filter(level__lte=max_user_level)
