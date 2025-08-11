# rbac/management/commands/assign_default_roles.py

from django.core.management.base import BaseCommand
from userservice.models import User
from rbac.models import Role, UserRole
from rbac.services import RoleAssignmentService


class Command(BaseCommand):
    help = 'Assign default role to all users without active roles'

    def handle(self, *args, **options):
        default_role = Role.objects.filter(is_default=True).first()
        if not default_role:
            self.stdout.write(self.style.ERROR("No default role found."))
            return

        users = User.objects.exclude(
            id__in=UserRole.objects.filter(is_active=True).values_list('user_id', flat=True)
        )

        count = 0
        for user in users:
            RoleAssignmentService.assign_role(user=user, role=default_role)
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Assigned default role to {count} users."))
