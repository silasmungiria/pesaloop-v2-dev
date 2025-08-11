from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from userservice.models import User
from rbac.models import Role, UserRole
from rbac.services import RoleAssignmentService


@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    """
    Ensure every user has at least one role.
    If not, assign the default role.
    """
    user = instance

    # Check if user already has an active role
    if UserRole.objects.filter(user=user, is_active=True).exists():
        return

    # Find the default role
    default_role = Role.objects.filter(is_default=True).first()
    if not default_role:
        # No default role set in the system
        return

    # Assign the default role
    RoleAssignmentService.assign_role(
        user=user,
        role=default_role,
        assigned_by=None  # Or system/admin user if preferred
    )
