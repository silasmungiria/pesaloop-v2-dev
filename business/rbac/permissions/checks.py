from django.utils import timezone
from .base import BaseAccessPermission


class MethodPermission(BaseAccessPermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        view_permission = f"{request.method.lower()}_permission"
        required_permission = getattr(view, view_permission, None)
        if not required_permission:
            required_permission = getattr(view, 'required_permission', None)

        if not required_permission:
            return False

        user_perms = self.get_user_permissions(request.user)

        has_access = (
            f"{required_permission}.{request.method.upper()}" in user_perms or
            f"{required_permission}.ALL" in user_perms
        )

        return has_access


class SensitiveOperationPermission(BaseAccessPermission):
    def has_permission(self, request, view):
        required_permission = self.get_required_permission(request, view)
        if not required_permission:
            return False

        from rbac.models import Permission
        is_sensitive = Permission.objects.filter(
            codename=required_permission,
            method__in=[request.method.upper(), 'ALL'],
            is_sensitive=True
        ).exists()

        if is_sensitive and not request.user.biometric_auth_enabled:
            self.log_access_attempt(request, required_permission, False)
            return False

        return True


class BusinessHoursAccessPermission(BaseAccessPermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        
        required_permission = self.get_required_permission(request, view)

        now = timezone.localtime(timezone.now())

        if now.weekday() >= 5 or not (9 <= now.hour < 15):
            self.log_access_attempt(request, required_permission, False)
            return False
        
        return True
