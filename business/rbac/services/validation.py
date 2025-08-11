from django.core.exceptions import ValidationError
from rbac.models import RolePermission

def validate_role_assignment(role, permission):
    """
    Validate if a permission can be assigned to a role
    """
    if RolePermission.objects.filter(role=role, permission=permission).exists():
        raise ValidationError("This permission is already assigned to the role")
    
    if role.level < permission.min_level:
        raise ValidationError(
            f"Role level ({role.level}) is too low for this permission "
            f"(requires level {permission.min_level})"
        )
